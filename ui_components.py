"""
Flet UI Components
Reimplementation of UI screens using Flet framework.
"""

import flet as ft
from typing import Callable, Dict, List, Optional
import time

class WelcomeScreen(ft.Column):
    def __init__(self, on_complete: Callable[[str, str], None]):
        super().__init__()
        self.on_complete = on_complete
        self.username_field = ft.TextField(
            label="اسم المستخدم / Username", 
            width=300,
            text_align=ft.TextAlign.RIGHT
        )
        self.language_dropdown = ft.Dropdown(
            label="اللغة / Language",
            width=300,
            options=[
                ft.dropdown.Option("arabic", "العربية"),
                ft.dropdown.Option("english", "English"),
            ],
            value="arabic"
        )
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 20
        
        self.controls = [
            ft.Text("مرحباً بك في مدرب الكتابة", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Welcome to Typing Speed Trainer", size=20),
            ft.Divider(height=20, color="transparent"),
            self.username_field,
            self.language_dropdown,
                ft.ElevatedButton(
                    "ابدأ / Start",
                    on_click=self.start_clicked,
                    width=200,
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.DEFAULT: "green"},
                    color={ft.ControlState.DEFAULT: "white"},
                )
                )
        ]

    def start_clicked(self, e):
        if not self.username_field.value:
            self.username_field.error_text = "الرجاء إدخال اسم المستخدم / Required"
            self.username_field.update()
            return
        
        self.on_complete(self.username_field.value, self.language_dropdown.value)


class MainMenu(ft.Column):
    def __init__(
        self, 
        user_data: Dict, 
        stats: Dict, 
        on_start_test: Callable, 
        on_manage_texts: Callable,
        on_view_stats: Callable,
        on_settings: Callable
    ):
        super().__init__()
        self.user_data = user_data
        self.stats = stats
        self.on_start_test = on_start_test
        self.on_manage_texts = on_manage_texts
        self.on_view_stats = on_view_stats
        self.on_settings = on_settings

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER

        self.controls = [
            ft.Text(f"مرحباً {self.user_data['username']}", size=30, weight=ft.FontWeight.BOLD),
            ft.Text(f"المستوى: {self.user_data.get('level', 1)}", size=20, color="blue200"),
            ft.Divider(),
            
            # Stats Summary
            ft.Row(
                controls=[
                    self._stat_card("الاختبارات", str(self.stats['total_tests'])),
                    self._stat_card("متوسط السرعة", f"{self.stats['average_wpm']} WPM"),
                    self._stat_card("متوسط الدقة", f"{self.stats['average_accuracy']}%"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            
            ft.Divider(height=40, color="transparent"),
            
            # Menu Buttons
            ft.Container(
                content=ft.Column(
                    controls=[
                        self._menu_button("بدء اختبار جديد / Start Test", ft.Icons.KEYBOARD, "green", self.on_start_test),
                        self._menu_button("إدارة النصوص / Manage Texts", ft.Icons.EDIT, "blue", self.on_manage_texts),
                        self._menu_button("الإحصائيات / Statistics", ft.Icons.BAR_CHART, "purple", self.on_view_stats),
                        self._menu_button("الإعدادات / Settings", ft.Icons.SETTINGS, "grey", self.on_settings),
                    ],
                    spacing=15
                ),
                width=400
            )
        ]

    def _stat_card(self, title, value):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=14, color="grey400"),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="surfaceVariant",
            padding=20,
            border_radius=10,
            width=150
        )

    def _menu_button(self, text, icon, color, on_click):
        return ft.ElevatedButton(
            text=text,
            icon=icon,
            on_click=lambda e: on_click(),
            height=50,
            width=400,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor={ft.ControlState.DEFAULT: "surfaceVariant"},
                color={ft.ControlState.DEFAULT: color},  # Text/Icon color
            )
        )

class ResultsScreen(ft.Column):
    def __init__(self, results: Dict, on_retry: Callable, on_home: Callable):
        super().__init__()
        self.results = results
        self.on_retry = on_retry
        self.on_home = on_home

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER

        score_color = "green" if self.results['overall_score'] >= 70 else "orange"
        
        self.controls = [
            ft.Text("نتيجة الاختبار / Test Results", size=30, weight=ft.FontWeight.BOLD),
            
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"{self.results['overall_score']}", size=60, weight=ft.FontWeight.BOLD, color=score_color),
                        ft.Text("النتيجة النهائية / Overall Score", size=16, color="grey400"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20
            ),
            
            ft.Row(
                controls=[
                    self._result_item("WPM", str(self.results['wpm']), "blue"),
                    self._result_item("Accuracy", f"{self.results['accuracy']}%", "green"),
                    self._result_item("Errors", str(self.results['incorrect_keystrokes']), "red"),
                    self._result_item("Time", f"{self.results['duration']}s", "orange"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            ),
            
            ft.Divider(height=20, color="transparent"),
            
            # Top Missed Keys
             ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("أكثر الحروف خطأ / Top Missed Keys", size=16, color="grey"),
                        ft.Row(
                            controls=[
                                self._missed_key_badge(char, count) 
                                for char, count in self.results.get('top_missed_keys', [])
                            ] if self.results.get('top_missed_keys') else [ft.Text("No errors! / لا يوجد أخطاء", color="green")],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10,
                border=ft.border.all(1, "grey200"),
                border_radius=10
            ),
            
            ft.Divider(height=40, color="transparent"),
            
            ft.Row(
                controls=[
                    ft.ElevatedButton("إعادة المحاولة / Retry", icon=ft.Icons.REFRESH, on_click=lambda e: self.on_retry()),
                    ft.OutlinedButton("القائمة الرئيسية / Main Menu", icon=ft.Icons.HOME, on_click=lambda e: self.on_home()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ]
    
    def _result_item(self, label, value, color):
        return ft.Column(
            controls=[
                ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(label, size=14, color="grey400"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _missed_key_badge(self, char, count):
        return ft.Container(
            content=ft.Row([
                ft.Text(f"'{char}'", size=20, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(f"{count}", size=14, color="white70")
            ], spacing=5),
            bgcolor="red400",
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
            border_radius=20
        )

class StatisticsScreen(ft.Column):
    def __init__(self, stats: Dict, on_back: Callable):
        super().__init__()
        self.stats = stats
        self.on_back = on_back
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        
        self.controls = [
            ft.Text("الإحصائيات / Statistics", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, color="transparent"),
            
            ft.Container(
                content=ft.Row(
                    controls=[
                         self._big_stat("Tests Taken", str(self.stats.get('total_tests', 0)), "blue"),
                         self._big_stat("Avg Speed", f"{self.stats.get('average_wpm', 0)} WPM", "green"),
                         self._big_stat("Avg Accuracy", f"{self.stats.get('average_accuracy', 0)}%", "purple"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=20
            ),
            
            ft.Divider(),
            
            ft.Text("Best Performances", size=20, weight=ft.FontWeight.BOLD),
            # Simple list of recent or best scores could go here, but for now just the summary
            
            ft.Container(height=50),
            
            ft.ElevatedButton(
                "رجوع / Back", 
                icon=ft.Icons.ARROW_BACK, 
                on_click=lambda e: self.on_back(),
                width=200
            )
        ]

    def _big_stat(self, label, value, color):
        return ft.Container(
            content=ft.Column(
                 controls=[
                     ft.Text(value, size=30, weight=ft.FontWeight.BOLD, color=color),
                     ft.Text(label, size=14, color="grey400")
                 ],
                 horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="surfaceVariant",
            padding=20,
            border_radius=15,
            width=180
        )

class SettingsScreen(ft.Column):
    def __init__(self, current_theme_mode: str, on_change_theme: Callable, on_back: Callable):
        super().__init__()
        self.current_theme_mode = current_theme_mode
        self.on_change_theme = on_change_theme
        self.on_back = on_back
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        
        self.theme_switch = ft.Switch(
            label="الوضع الليلي / Dark Mode", 
            value=(current_theme_mode == "dark"),
            on_change=self.theme_changed
        )
        
        self.controls = [
            ft.Text("الإعدادات / Settings", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, color="transparent"),
            
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("المظهر / Appearance", size=20, weight=ft.FontWeight.BOLD),
                        self.theme_switch,
                    ]
                ),
                bgcolor="surfaceVariant",
                padding=20,
                border_radius=10,
                width=400
            ),
            
            ft.Divider(height=40, color="transparent"),
            
            ft.ElevatedButton(
                "رجوع / Back", 
                icon=ft.Icons.ARROW_BACK, 
                on_click=lambda e: self.on_back(),
                width=200
            )
        ]

    def theme_changed(self, e):
        mode = "dark" if self.theme_switch.value else "light"
        self.on_change_theme(mode)

class ManageTextsScreen(ft.Column):
    def __init__(self, data_manager, on_back: Callable):
        super().__init__()
        self.data_manager = data_manager
        self.on_back = on_back
        
        self.english_texts_list = ft.ListView(expand=True, spacing=10)
        self.arabic_texts_list = ft.ListView(expand=True, spacing=10)
        
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Arabic / العربية", content=self.build_tab_content("arabic")),
                ft.Tab(text="English / الإنجليزية", content=self.build_tab_content("english")),
            ],
            expand=True
        )
        
        self.controls = [
            ft.Row([
                ft.Text("إدارة النصوص / Manage Texts", size=30, weight=ft.FontWeight.BOLD),
                ft.IconButton(ft.Icons.HOME, on_click=lambda e: self.on_back())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Container(
                content=self.tabs,
                expand=True
            )
        ]
    
    def build_tab_content(self, language):
        # List Container
        list_view = self.arabic_texts_list if language == "arabic" else self.english_texts_list
        self.refresh_list(language)
        
        # Add Input
        text_input = ft.TextField(label="نص جديد / New Text", multiline=True, min_lines=2, expand=True)
        difficulty_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("beginner", "مبتدئ / Beginner"),
                ft.dropdown.Option("intermediate", "متوسط / Intermediate"),
                ft.dropdown.Option("advanced", "متقدم / Advanced"),
            ],
            value="intermediate",
            width=150
        )
        
        def add_clicked(e):
            if not text_input.value:
                return
            
            self.data_manager.add_custom_text(language, text_input.value, difficulty_dropdown.value)
            text_input.value = ""
            text_input.update()
            self.refresh_list(language)
            
        add_container = ft.Column([
            ft.Text("إضافة نص جديد / Add New Text", weight=ft.FontWeight.BOLD),
            ft.Row([
                text_input,
                difficulty_dropdown,
                ft.IconButton(ft.Icons.ADD_CIRCLE, icon_color="green", on_click=add_clicked, tooltip="Add")
            ])
        ], spacing=10)

        return ft.Column([
            add_container,
            ft.Divider(),
            ft.Text("قائمة النصوص (تظهر النصوص المضافة فقط) / Custom Texts", color="grey"),
            list_view
        ], expand=True, spacing=20, scroll=ft.ScrollMode.HIDDEN)

    def refresh_list(self, language):
        list_view = self.arabic_texts_list if language == "arabic" else self.english_texts_list
        list_view.controls.clear()
        
        texts = self.data_manager.get_texts(language)
        # Filter for custom only? Or show all?
        # Ideally only custom ones are deletable.
        
        custom_texts = [t for t in texts if t.get("custom", False)]
        
        if not custom_texts:
            list_view.controls.append(ft.Text("لا يوجد نصوص مضافة / No custom texts found", italic=True, text_align=ft.TextAlign.CENTER))
        
        for text in custom_texts:
            t = text # capture for closure
            list_view.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(t["text"][:50] + "..." if len(t["text"]) > 50 else t["text"], weight=ft.FontWeight.BOLD),
                            ft.Text(f"Difficulty: {t.get('difficulty')} | ID: {t['id']}", size=12, color="grey")
                        ], expand=True),
                        ft.IconButton(
                            ft.Icons.DELETE, 
                            icon_color="red", 
                            on_click=lambda e, lang=language, tid=t["id"]: self.delete_text(lang, tid)
                        )
                    ]),
                    bgcolor="surfaceVariant",
                    padding=10,
                    border_radius=5
                )
            )
        if list_view.page:
            list_view.update()

    def delete_text(self, language, text_id):
        self.data_manager.delete_custom_text(language, text_id)
        self.refresh_list(language)
