"""
Data Manager Module
Handles all data persistence operations including user profiles, texts, and results.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class DataManager:
    """Manages all data storage and retrieval operations."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.texts_arabic_file = os.path.join(data_dir, "texts_arabic.json")
        self.texts_english_file = os.path.join(data_dir, "texts_english.json")
        self.results_file = os.path.join(data_dir, "results.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data files
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize data files with default content if they don't exist."""
        # Initialize users file
        if not os.path.exists(self.users_file):
            self._save_json(self.users_file, {})
        
        # Initialize Arabic texts
        if not os.path.exists(self.texts_arabic_file):
            default_arabic_texts = {
                "beginner": [
                    {"id": "ar_b_001", "text": "السلام عليكم ورحمة الله وبركاته", "difficulty": "beginner"},
                    {"id": "ar_b_002", "text": "الحمد لله رب العالمين", "difficulty": "beginner"},
                    {"id": "ar_b_003", "text": "بسم الله الرحمن الرحيم", "difficulty": "beginner"},
                    {"id": "ar_b_004", "text": "العلم نور والجهل ظلام", "difficulty": "beginner"},
                    {"id": "ar_b_005", "text": "الصبر مفتاح الفرج", "difficulty": "beginner"},
                ],
                "intermediate": [
                    {"id": "ar_i_001", "text": "التعليم هو السلاح الأقوى الذي يمكنك استخدامه لتغيير العالم", "difficulty": "intermediate"},
                    {"id": "ar_i_002", "text": "النجاح ليس نهاية والفشل ليس قاتلا إنها الشجاعة للاستمرار هي التي تهم", "difficulty": "intermediate"},
                    {"id": "ar_i_003", "text": "الطريق إلى النجاح دائما تحت الإنشاء", "difficulty": "intermediate"},
                    {"id": "ar_i_004", "text": "لا تقل أبدا أنك لا تستطيع فعل شيء ما قبل أن تحاول", "difficulty": "intermediate"},
                    {"id": "ar_i_005", "text": "القراءة تصنع إنسانا كاملا والمناقشة تصنع إنسانا مستعدا والكتابة تصنع إنسانا دقيقا", "difficulty": "intermediate"},
                ],
                "advanced": [
                    {"id": "ar_a_001", "text": "إن الذين آمنوا وعملوا الصالحات كانت لهم جنات الفردوس نزلا خالدين فيها لا يبغون عنها حولا", "difficulty": "advanced"},
                    {"id": "ar_a_002", "text": "العلم في الصغر كالنقش على الحجر والعلم في الكبر كالنقش على الماء فاغتنم فرصة التعلم في شبابك", "difficulty": "advanced"},
                    {"id": "ar_a_003", "text": "إذا أردت أن تكون ناجحا فعليك أن تحترم قاعدة واحدة لا تكذب أبدا على نفسك", "difficulty": "advanced"},
                    {"id": "ar_a_004", "text": "الحياة مثل ركوب الدراجة للحفاظ على توازنك يجب أن تستمر في التحرك", "difficulty": "advanced"},
                    {"id": "ar_a_005", "text": "المعرفة قوة والمعلومات حرية والتعليم هو مقدمة التقدم في كل مجتمع وفي كل عائلة", "difficulty": "advanced"},
                ]
            }
            self._save_json(self.texts_arabic_file, default_arabic_texts)
        
        # Initialize English texts
        if not os.path.exists(self.texts_english_file):
            default_english_texts = {
                "beginner": [
                    {"id": "en_b_001", "text": "The quick brown fox jumps over the lazy dog", "difficulty": "beginner"},
                    {"id": "en_b_002", "text": "Practice makes perfect", "difficulty": "beginner"},
                    {"id": "en_b_003", "text": "Hello world welcome to typing", "difficulty": "beginner"},
                    {"id": "en_b_004", "text": "Learning to type is fun", "difficulty": "beginner"},
                    {"id": "en_b_005", "text": "Speed and accuracy matter", "difficulty": "beginner"},
                ],
                "intermediate": [
                    {"id": "en_i_001", "text": "Education is the most powerful weapon which you can use to change the world", "difficulty": "intermediate"},
                    {"id": "en_i_002", "text": "Success is not final failure is not fatal it is the courage to continue that counts", "difficulty": "intermediate"},
                    {"id": "en_i_003", "text": "The only way to do great work is to love what you do", "difficulty": "intermediate"},
                    {"id": "en_i_004", "text": "Believe you can and you are halfway there", "difficulty": "intermediate"},
                    {"id": "en_i_005", "text": "The future belongs to those who believe in the beauty of their dreams", "difficulty": "intermediate"},
                ],
                "advanced": [
                    {"id": "en_a_001", "text": "In the midst of chaos there is also opportunity and the wise man will find a way to turn obstacles into stepping stones", "difficulty": "advanced"},
                    {"id": "en_a_002", "text": "The greatest glory in living lies not in never falling but in rising every time we fall", "difficulty": "advanced"},
                    {"id": "en_a_003", "text": "Life is what happens when you are busy making other plans so embrace the unexpected", "difficulty": "advanced"},
                    {"id": "en_a_004", "text": "The only impossible journey is the one you never begin so take that first step today", "difficulty": "advanced"},
                    {"id": "en_a_005", "text": "Knowledge is power information is liberating education is the premise of progress in every society", "difficulty": "advanced"},
                ]
            }
            self._save_json(self.texts_english_file, default_english_texts)
        
        # Initialize results file
        if not os.path.exists(self.results_file):
            self._save_json(self.results_file, [])
    
    def _load_json(self, filepath: str) -> Dict:
        """Load JSON data from file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}
    
    def _save_json(self, filepath: str, data):
        """Save data to JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
    
    # User Management
    def user_exists(self) -> bool:
        """Check if a user profile exists."""
        user_data = self._load_json(self.users_file)
        return bool(user_data.get("username"))
    
    def create_user(self, username: str, language: str = "english") -> Dict:
        """Create a new user profile."""
        user_data = {
            "username": username,
            "language": language,
            "level": 1,
            "total_tests": 0,
            "created_at": datetime.now().isoformat()
        }
        self._save_json(self.users_file, user_data)
        return user_data
    
    def get_user(self) -> Optional[Dict]:
        """Get user profile."""
        user_data = self._load_json(self.users_file)
        return user_data if user_data.get("username") else None
    
    def update_user(self, **kwargs):
        """Update user profile."""
        user_data = self._load_json(self.users_file)
        user_data.update(kwargs)
        self._save_json(self.users_file, user_data)
    
    # Text Management
    def get_texts(self, language: str, difficulty: str = None) -> List[Dict]:
        """Get texts for a specific language and optional difficulty."""
        if language == "arabic":
            texts_data = self._load_json(self.texts_arabic_file)
        else:
            texts_data = self._load_json(self.texts_english_file)
        
        if difficulty:
            return texts_data.get(difficulty, [])
        else:
            # Return all texts
            all_texts = []
            for diff_texts in texts_data.values():
                all_texts.extend(diff_texts)
            return all_texts
    
    def add_custom_text(self, language: str, text: str, difficulty: str = "intermediate"):
        """Add a custom text to the library."""
        if language == "arabic":
            filepath = self.texts_arabic_file
        else:
            filepath = self.texts_english_file
        
        texts_data = self._load_json(filepath)
        
        # Generate unique ID
        custom_id = f"{language[:2]}_custom_{len(texts_data.get(difficulty, []))}"
        
        new_text = {
            "id": custom_id,
            "text": text,
            "difficulty": difficulty,
            "custom": True
        }
        
        if difficulty not in texts_data:
            texts_data[difficulty] = []
        
        texts_data[difficulty].append(new_text)
        self._save_json(filepath, texts_data)
    
    def delete_custom_text(self, language: str, text_id: str):
        """Delete a custom text."""
        if language == "arabic":
            filepath = self.texts_arabic_file
        else:
            filepath = self.texts_english_file
        
        texts_data = self._load_json(filepath)
        
        for difficulty in texts_data:
            texts_data[difficulty] = [
                t for t in texts_data[difficulty] 
                if t["id"] != text_id or not t.get("custom", False)
            ]
        
        self._save_json(filepath, texts_data)
    
    # Results Management
    def save_result(self, result: Dict):
        """Save a test result."""
        results = self._load_json(self.results_file)
        result["timestamp"] = datetime.now().isoformat()
        results.append(result)
        self._save_json(self.results_file, results)
        
        # Update user stats
        user = self.get_user()
        if user:
            total_tests = user.get("total_tests", 0) + 1
            self.update_user(total_tests=total_tests)
            
            # Update level based on performance
            overall_score = result.get("overall_score", 0)
            if overall_score > user.get("level", 1):
                self.update_user(level=min(100, int(overall_score)))
    
    def get_results(self, limit: int = None) -> List[Dict]:
        """Get test results, optionally limited to most recent."""
        results = self._load_json(self.results_file)
        if limit:
            return results[-limit:]
        return results
    
    def get_statistics(self) -> Dict:
        """Calculate statistics from all results."""
        results = self.get_results()
        
        if not results:
            return {
                "total_tests": 0,
                "average_wpm": 0,
                "average_accuracy": 0,
                "best_wpm": 0,
                "best_accuracy": 0,
                "total_time": 0
            }
        
        total_wpm = sum(r.get("wpm", 0) for r in results)
        total_accuracy = sum(r.get("accuracy", 0) for r in results)
        total_time = sum(r.get("duration", 0) for r in results)
        
        return {
            "total_tests": len(results),
            "average_wpm": round(total_wpm / len(results), 1),
            "average_accuracy": round(total_accuracy / len(results), 1),
            "best_wpm": max(r.get("wpm", 0) for r in results),
            "best_accuracy": max(r.get("accuracy", 0) for r in results),
            "total_time": total_time
        }
