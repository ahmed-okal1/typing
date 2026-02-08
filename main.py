
import flet as ft
from data_manager import DataManager
from typing_test import TypingTest
from ui_components import WelcomeScreen, MainMenu, ResultsScreen, StatisticsScreen, SettingsScreen, ManageTextsScreen
from flet_typing_screen import TypingTestScreen
import random

def main(page: ft.Page):
    # App Configuration
    page.title = "Typing Speed Trainer - مدرب الكتابة السريعة"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        "Amiri": "https://fonts.googleapis.com/css2?family=Amiri&display=swap"
    }
    
    # Data Manager
    data_manager = DataManager()
    
    # State
    state = {
        "user": None,
        "current_test": None,
        "current_text": None,
        "quran_info": None, # Optional: {surah_id: int, char_start: int}
    }

    # Navigation Methods
    def show_welcome():
        page.clean()
        page.add(WelcomeScreen(on_complete=on_welcome_complete))

    def on_welcome_complete(username, language):
        user = data_manager.create_user(username, language)
        state["user"] = user
        show_menu()
    def show_menu():
        page.clean()
        # Unsubscribe from keyboard events just in case
        page.on_keyboard_event = None
        
        user = data_manager.get_user()
        stats = data_manager.get_statistics()
        
        progress = data_manager.get_quran_progress()
        has_progress = progress and progress.get("char_index", 0) > 0
        
        page.add(MainMenu(
            user_data=user,
            stats=stats,
            on_start_test=lambda: show_text_selection(),
            on_manage_texts=lambda: show_manage_texts(),
            on_view_stats=lambda: show_stats(),
            on_settings=lambda: show_settings(),
            on_resume_quran=lambda: resume_quran() if has_progress else None
        ))

    def resume_quran():
        progress = data_manager.get_quran_progress()
        start_quran_test(progress["surah_id"], progress["char_index"])

    def start_quran_test(surah_id, char_start):
        chunk_info = data_manager.get_surah_chunk(surah_id, char_start)
        if not chunk_info:
            page.open(ft.SnackBar(ft.Text("لقد انتهت السورة! / Surah completed!")))
            show_menu()
            return
            
        state["current_text"] = {
            "id": f"quran_{surah_id}_{char_start}",
            "text": chunk_info["text"],
            "difficulty": "advanced"
        }
        state["quran_info"] = {
            "surah_id": surah_id,
            "char_start": char_start,
            "is_last": chunk_info["is_last"]
        }
        state["current_test"] = TypingTest(chunk_info["text"])
        show_typing_screen()

    def show_text_selection():
        # Language selection
        lang_dropdown = ft.Dropdown(
            label="اللغة / Language",
            options=[
                ft.dropdown.Option("arabic", "العربية"),
                ft.dropdown.Option("english", "English"),
            ],
            value=state["user"].get("language", "arabic"),
            width=200
        )

        def start_test(difficulty):
            page.close(dialog)
            page.update()
            
            # Update language based on selection
            selected_lang = lang_dropdown.value
            state["user"]["language"] = selected_lang
            if data_manager.user_exists():
                 # Optional: Update user file if we had a method for it, 
                 # for now just session state is enough or re-save user
                 pass

            texts = data_manager.get_texts(selected_lang, difficulty)
            if not texts:
                print(f"DEBUG: No texts found for {selected_lang} - {difficulty}")
                page.open(ft.SnackBar(ft.Text(f"No texts found for {selected_lang}")))
                return 
                
            text_obj = random.choice(texts)
            state["current_text"] = text_obj
            state["current_test"] = TypingTest(text_obj["text"])
            
            print(f"DEBUG: Starting test with text: {text_obj['text'][:20]}...")
            show_typing_screen()

        dialog = ft.AlertDialog(
            title=ft.Text("إعدادات الاختبار / Test Settings"),
            content=ft.Column([
                lang_dropdown,
                ft.Divider(),
                ft.Text("اختر النوع / Select Type"),
                ft.ElevatedButton("مستويات القرآن / Quran Levels", on_click=lambda e: show_quran_selection(dialog), width=250, color="orange"),
                ft.Divider(),
                ft.Text("أو اختر مستوى عشوائي / Or Select Random Level"),
                ft.Row([
                    ft.ElevatedButton("مبتدئ / Beginner", on_click=lambda e: start_test("beginner")),
                    ft.ElevatedButton("متوسط / Intermediate", on_click=lambda e: start_test("intermediate")),
                    ft.ElevatedButton("متقدم / Advanced", on_click=lambda e: start_test("advanced")),
                ], wrap=True, alignment=ft.MainAxisAlignment.CENTER),
            ], height=350, alignment=ft.MainAxisAlignment.CENTER),
        )
        page.open(dialog)

    def show_quran_selection(parent_dialog=None):
        if parent_dialog:
            page.close(parent_dialog)
        surahs = data_manager.get_surah_list()
        
        def on_surah_select(surah_id):
            page.close(dialog)
            # Ask if start from beginning or specific ayah? 
            # Simplest for now: Ask for starting char or just start from beginning.
            # User requested: "يعرض البداية من البداية او من ابتداء من ايه معينة"
            # Since my logic is char-based, I'll provide an option to start from an Ayah by looking up its offset.
            show_ayah_selection(surah_id)

        surah_buttons = [
            ft.ListTile(
                title=ft.Text(f"{s['id']}. {s['name']}"),
                on_click=lambda e, sid=s["id"]: on_surah_select(sid)
            ) for s in surahs
        ]

        dialog = ft.AlertDialog(
            title=ft.Text("اختر السورة / Select Surah"),
            content=ft.Container(
                content=ft.ListView(controls=surah_buttons, height=400),
                width=300
            )
        )
        page.open(dialog)

    def show_ayah_selection(surah_id):
        raw_data = data_manager._load_json(data_manager.quran_raw_file)
        surah = next(s for s in raw_data if s["id"] == surah_id)
        
        def start_from_ayah(ayah_index):
            page.close(dialog)
            # Calculate char offset
            full_text_before = " ".join([surah["verses"][i]["text"] for i in range(ayah_index)])
            # Clean it to get accurate offset
            cleaned_before = data_manager.clean_quran_text(full_text_before)
            
            if ayah_index == 0:
                offset = 0
            else:
                # Add 1 for the space that was used in joining if there was text before
                offset = len(cleaned_before) + 1
            
            start_quran_test(surah_id, offset)

        ayah_buttons = [
            ft.ListTile(
                title=ft.Text(f"آية {v['id']}"),
                subtitle=ft.Text(v["text"][:30] + "...", size=12),
                on_click=lambda e, idx=i: start_from_ayah(idx)
            ) for i, v in enumerate(surah["verses"])
        ]

        dialog = ft.AlertDialog(
            title=ft.Text(f"اختر بداية الكتابة - {surah['name']}"),
            content=ft.Container(
                content=ft.ListView(controls=ayah_buttons, height=400),
                width=300
            )
        )
        page.open(dialog)

    def show_typing_screen():
        page.clean()
        
        # Wrap screen in container
        lang = state["user"].get("language", "english")
        text = state["current_text"]["text"]
        
        # Event handler bridging Flet UI events to TypingTest logic
        def on_event(event_type, data):
            test = state["current_test"]
            
            if event_type == "start":
                test.start()
            elif event_type == "keystroke":
                result = test.process_keystroke(data.get("char"), data.get("is_backspace"))
                result["test_complete"] = test.is_test_complete()
                return result
            elif event_type == "update":
                return test.get_current_stats()
            elif event_type == "finish":
                test.finish()
                if state.get("quran_info"):
                    # Save progress to EXACTLY the next start point
                    q_info = state["quran_info"]
                    data_manager.save_quran_progress(q_info["surah_id"], q_info["char_start"] + len(text) + 1)
                show_results()
            elif event_type == "restart":
                # reset test
                state["current_test"] = TypingTest(text)
                show_typing_screen()
            elif event_type == "home":
                state["quran_info"] = None # Clear quran context on home
                show_menu()
        
        screen = TypingTestScreen(text, lang, on_event)
        page.add(screen)
        
        # Bind global keyboard event to screen handler
        print("DEBUG: Binding keyboard event")
        page.on_keyboard_event = screen.handle_keystroke
        page.update()
        
    def show_results():
        page.on_keyboard_event = None # Stop listening
        page.clean()
        
        results = state["current_test"].calculate_scores()
        
        # Save results
    def restart_test():
        # Quick restart with same settings
        current_text = state["current_text"]
        difficulty = current_text.get("difficulty", "intermediate")
        lang = state["user"].get("language", "arabic")
        
        # Optionally pick a NEW text of same difficulty
        texts = data_manager.get_texts(lang, difficulty)
        if texts:
            text_obj = random.choice(texts)
            state["current_text"] = text_obj
            state["current_test"] = TypingTest(text_obj["text"])
            show_typing_screen()
        else:
            show_text_selection() # Fallback

    def show_results():
        page.on_keyboard_event = None # Stop listening
        page.clean()
        
        results = state["current_test"].calculate_scores()
        
        # Save results
        raw_result = {
            "language": state["user"].get("language", "english"),
            "text_id": state["current_text"]["id"],
            "difficulty": state["current_text"].get("difficulty", "intermediate"),
            **results
        }
        data_manager.save_result(raw_result)
        
        on_next = None
        if state.get("quran_info"):
            q_info = state["quran_info"]
            if not q_info.get("is_last"):
                next_start = q_info["char_start"] + len(state["current_text"]["text"]) + 1 # +1 for the space joining
                on_next = lambda: start_quran_test(q_info["surah_id"], next_start)
        
        # Keyboard shortcut for Results page
        def handle_results_key(e: ft.KeyboardEvent):
            if e.key == " ":
                page.on_keyboard_event = None # Unbind
                if on_next:
                    on_next()
                else:
                    restart_test() # Default to retry for normal tests
        
        page.on_keyboard_event = handle_results_key

        page.add(ResultsScreen(
            results,
            on_retry=lambda: restart_test(), # Direct restart
            on_home=lambda: show_menu(),
            on_next=on_next
        ))
        page.update()

    # Placeholder pages
    # Placeholder pages
    def show_manage_texts():
        page.clean()
        page.add(ManageTextsScreen(
            data_manager=data_manager,
            on_back=lambda: show_menu()
        ))
        
    def show_stats():
        page.clean()
        stats = data_manager.get_statistics()
        page.add(StatisticsScreen(
            stats=stats,
            on_back=lambda: show_menu()
        ))
        
    def show_settings():
        page.clean()
        current_theme = "dark" if page.theme_mode == ft.ThemeMode.DARK else "light"
        
        def change_theme(mode):
            page.theme_mode = ft.ThemeMode.DARK if mode == "dark" else ft.ThemeMode.LIGHT
            page.update()
            
        page.add(SettingsScreen(
            current_theme_mode=current_theme,
            on_change_theme=change_theme,
            on_back=lambda: show_menu()
        ))

    # Init
    if data_manager.user_exists():
        state["user"] = data_manager.get_user()
        show_menu()
    else:
        show_welcome()

if __name__ == "__main__":
    ft.app(target=main)
