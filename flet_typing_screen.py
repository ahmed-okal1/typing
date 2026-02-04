
import flet as ft
from typing import Callable, Dict

class TypingTestScreen(ft.Column):
    def __init__(self, text: str, language: str, on_event: Callable):
        super().__init__()
        self.text = text
        self.language = language
        self.on_event = on_event
        
        self.spacing = 10
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.text_display = ft.Text(
            spans=[], 
            size=24, 
            weight=ft.FontWeight.W_500,
            font_family="Arial" if language == "arabic" else "Roboto Mono",
            text_align=ft.TextAlign.RIGHT if language == "arabic" else ft.TextAlign.LEFT
        )
        
        # Stats controls
        self.time_text = ft.Text("0s", size=20, weight=ft.FontWeight.BOLD, color="orange")
        self.wpm_text = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, color="blue")
        self.acc_text = ft.Text("100%", size=20, weight=ft.FontWeight.BOLD, color="green")
        self.error_text = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, color="red")
        
        self.audio_error = ft.Audio(src="https://www.soundjay.com/buttons/sounds/button-10.mp3", autoplay=False)
        self.overlay = ft.Container(content=self.audio_error, width=0, height=0)
        
        self.hidden_input_ref = ft.Ref[ft.TextField]()
        self.text_display.spans = self._generate_spans({})
        
        self.controls = [
            self.overlay,
            # Stats Header
            ft.Container(
                content=ft.Row(
                    controls=[
                        self._stat_box("Time", self.time_text),
                        self._stat_box("WPM", self.wpm_text),
                        self._stat_box("Accuracy", self.acc_text),
                        self._stat_box("Errors", self.error_text),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                bgcolor="surfaceVariant",
                padding=15,
                border_radius=10,
            ),
            ft.Divider(height=20, color="transparent"),
            
            # Navigation Buttons
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "إعادة البدء / Restart", 
                        icon=ft.Icons.REFRESH, 
                        on_click=lambda e: self.on_event("restart", None),
                        color="white",
                        bgcolor="blue"
                    ),
                    ft.OutlinedButton(
                        "القائمة الرئيسية / Home", 
                        icon=ft.Icons.HOME, 
                        on_click=lambda e: self.on_event("home", None)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),

            # Text Display Area - Click to focus
            ft.Container(
                content=self.text_display,
                padding=30,
                bgcolor="surfaceVariant",
                border_radius=15,
                border=ft.border.all(2, "outlineVariant"),
                width=900,
                alignment=ft.alignment.top_right if self.language == "arabic" else ft.alignment.top_left,
                on_click=lambda e: self.focus_input()
            ),
            
            # Hidden Input Field
            ft.Container(
                content=ft.TextField(
                    width=0, 
                    height=0, 
                    opacity=0, 
                    on_change=self.handle_input_change,
                    ref=self.hidden_input_ref,
                    autofocus=True
                ),
                width=0, height=0
            ),
            
            ft.Text(
                "اضغط على النص وابدأ الكتابة... / Click text to start typing...", 
                color="grey500",
                italic=True
            )
        ]
        
        # Start the test immediately
        self.on_event("start", None)

    def focus_input(self):
        if self.hidden_input_ref.current:
            self.hidden_input_ref.current.focus()
            self.text_display.parent.border = ft.border.all(2, "blue")
            self.text_display.parent.update()

    def _stat_box(self, label, control):
        return ft.Column(
            controls=[
                ft.Text(label, size=12, color="grey400"),
                control
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def play_error_sound(self):
        # Flet Audio control needs to be released/seeked to play again usually, 
        # or we just create a new one. For simplicity let's try calling update.
        # In a real app we might use a pool or just a simple beep.
        # Since local file play might be tricky with path, using web url for generic beep or handled by native
        # For now, let's skip actual audio or rely on visual feedback mostly as audio in web-based/flet can be tricky without assets.
        # We'll just flash the border red visually (logic in update)
        pass

    def handle_input_change(self, e):
        # Determine the change (this is a bit tricky with on_change as it gives full value)
        # But for typing test we can just clear it after reading?
        # Or keeping it to support backspace?
        # ISSUE: If we clear it, Mobile/IME might struggle.
        # Better strategy: Compare current value with previous known value?
        # Simplified strategy: 
        # For every character typed, we get the whole string. 
        # But we only want the *last* action.
        # Actually simplest for typing test: 
        # Just clear the text field after processing the last char? 
        # But that breaks Arabic composition.
        # So we keep the text in the field, and we check the *difference*.
        
        current_val = e.control.value
        if not current_val:
            return
            
        # Get the new character(s)
        # This is a basic implementation assuming 1 char at a time usually
        # For backspace, the length will decrease.
        
        last_char = current_val[-1]
        
        # Handle "Space" specifically if needed, but in TextField ' ' is just ' '
        
        # We need to detect Backspace. 
        # Flet TextField doesn't easily convert Backspace to a character event here, 
        # but the string length shrinks.
        # However, we don't have previous state easily here without storing it in class.
        # Let's rely on storing `self.last_input_len`.
        
        # WAIT: The simplest way that works for most is to just clear it?
        # No, Arabic connected letters depend on history.
        
        # Let's try this: 
        # Rely on the fact that we process one char at a time.
        # Actually, handling Backspace via on_change is hard (detection of deletion).
        # We might need `on_keyboard_event` for control keys (Backspace) 
        # and `on_change` (or `on_submit`?) for text.
        # Combined approach:
        # 1. Listen to `on_change` for characters.
        # 2. Listen to `on_keyboard_event` ONLY for Backspace?
        #    But `on_keyboard_event` on Page captures everything.
        
        # Let's look at the logs again: Backspace WAS detected correctly in `on_keyboard_event`.
        # The problem was just the characters.
        # So: Use `on_keyboard_event` for Backspace.
        # Use `TextField` for Characters?
        # But TextField also consumes the key press, so `on_keyboard_event` might fire too?
        
        # Strategy:
        # Use a TextField. 
        # In its `on_change`: take the last character, process it, then CLEAR the text field?
        # If I clear it, Arabic simple typing usually works fine (connecting letters might flicker but usually logic handles it).
        # Ligatures are visual. If I type 'l' then 'a', I get 'la'. 
        # If I clear 'l' then type 'a', I get 'a'.
        # This breaks visual composition in the input field, but we are displaying the text in OUR custom display.
        # Our custom display handles the full string logic.
        # The input field is hidden anyway!
        # So clearing it is fine! 
        # EXCEPT for Android/Mobile keyboards which might get confused if field is cleared.
        # But on Desktop Windows, clearing should be fine.
        
        # Let's try: 
        # 1. Get char.
        # 2. Process.
        # 3. Clear text field.
        
        # What about Backspace? `on_change` doesn't fire for backspace if empty?
        # We need `on_keyboard_event` on the TextField? Flet TextField doesn't export that directly?
        # We can use `on_submit`? No.
        
        # We can use the Page's keyboard event for Backspace (it works global).
        # And use TextField for characters.
        
        # So:
        # global handle_keystroke:
        #   if key == "Backspace": process backspace.
        #   else: ignore (let TextField handle it).
        
        # TextField on_change:
        #   char = value
        #   process char
        #   value = ""
        
        new_char = current_val[-1]
        data = {"char": new_char, "is_backspace": False}
        self.process_input(data)
        
        e.control.value = ""
        e.control.update()

    def handle_global_key(self, e: ft.KeyboardEvent):
        if e.key == "Backspace":
             self.process_input({"char": "", "is_backspace": True})

    def process_input(self, data):
        result = self.on_event("keystroke", data)
        if result:
            if not result.get("accepted", True) or result.get("error", False):
                self.text_display.parent.border = ft.border.all(2, "red")
                self.text_display.parent.update()
            else:
                self.text_display.parent.border = ft.border.all(2, "blue") # Keep blue focus
            
            self.update_display()
            
            if result.get("test_complete", False):
                self.on_event("finish", None)
                
    # Retain old handle_keystroke just in case but rename or delete
    # We need to register handle_global_key instead of handle_keystroke in main.py? 
    # Or just call it handle_keystroke and change logic.
    
    def handle_keystroke(self, e: ft.KeyboardEvent):
        # We only care about Backspace here now
        if e.key == "Backspace":
             self.process_input({"char": "", "is_backspace": True})
        # Ignore other keys, let Hidden TextField handle them

    def update_display(self):
        stats = self.on_event("update", None)
        if stats:
            self.update_text_display(stats)
            self.time_text.value = f"{stats['elapsed_time']}s"
            self.wpm_text.value = f"{stats['current_wpm']}"
            self.acc_text.value = f"{stats['current_accuracy']}%"
            self.error_text.value = f"{stats['errors']}"
            self.update()

    def update_text_display(self, stats: Dict):
        self.text_display.spans = self._generate_spans(stats)
        # Assuming run via update_display which calls self.update()
        
    def _generate_spans(self, stats: Dict):
        words = self.text.split()
        completed_count = stats.get("words_completed", 0)
        current_input = stats.get("current_word_input", "")
        
        # Build spans
        spans = []
        
        for i, word in enumerate(words):
            # Space between words
            if i > 0:
                spans.append(ft.TextSpan(" "))
            
            if i < completed_count:
                # Completed Word
                spans.append(ft.TextSpan(word, ft.TextStyle(color="green")))
            
            elif i == completed_count:
                # Current Word (Partial coloring)
                # Correct part
                correct_len = 0
                for j, char in enumerate(word):
                    if j < len(current_input):
                        if current_input[j] == char:
                           spans.append(ft.TextSpan(char, ft.TextStyle(color="green", bgcolor=None)))
                        else:
                           spans.append(ft.TextSpan(char, ft.TextStyle(color="red", bgcolor="red100")))
                    else:
                        if j == len(current_input):
                            # Current character cursor
                            spans.append(ft.TextSpan(char, ft.TextStyle(bgcolor="grey700", color="white")))
                        else:
                            # Pending characters
                             spans.append(ft.TextSpan(char, ft.TextStyle(color="grey")))
            else:
                # Pending Word
                spans.append(ft.TextSpan(word, ft.TextStyle(color="grey700")))
        return spans
