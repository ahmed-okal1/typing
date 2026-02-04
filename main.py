
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
        
        page.add(MainMenu(
            user_data=user,
            stats=stats,
            on_start_test=lambda: show_text_selection(),
            on_manage_texts=lambda: show_manage_texts(),
            on_view_stats=lambda: show_stats(),
            on_settings=lambda: show_settings()
        ))

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
                ft.Text("اختر الصعوبة / Select Difficulty"),
                ft.ElevatedButton("مبتدئ / Beginner", on_click=lambda e: start_test("beginner"), width=200),
                ft.ElevatedButton("متوسط / Intermediate", on_click=lambda e: start_test("intermediate"), width=200),
                ft.ElevatedButton("متقدم / Advanced", on_click=lambda e: start_test("advanced"), width=200),
            ], height=250, alignment=ft.MainAxisAlignment.CENTER),
        )
        page.open(dialog)
        print("DEBUG: Dialog opened")

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
                show_results()
            elif event_type == "restart":
                # reset test
                state["current_test"] = TypingTest(text)
                show_typing_screen()
            elif event_type == "home":
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
        
        page.add(ResultsScreen(
            results,
            on_retry=lambda: restart_test(), # Direct restart
            on_home=lambda: show_menu()
        ))

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
