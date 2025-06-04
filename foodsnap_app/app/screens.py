# screens.py
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from app.utils.classifier import FoodClassifier
from app.utils.apis import get_nutrition, get_recipe
import threading
import os

class MainScreen(Screen):
    def snap_food(self):
        from plyer import camera
        fn = os.path.join(self.manager.app.user_data_dir, "last_pic.jpg")
        camera.take_picture(filename=fn, on_complete=lambda x: self.process_image(x))

    @mainthread
    def process_image(self, image_path):
        self.ids.result_label.text = "Analyzing that tasty @#$%!..."
        def _worker():
            clf = self.manager.app.classifier
            results = clf.predict(image_path, top_k=1)
            if not results:
                self.show_error("Classifier flopped. Try again, genius.")
                return
            label, conf = results[0]
            nutri = get_nutrition(label)
            recipes = get_recipe(label)
            self.update_results(label, conf, nutri, recipes)
        threading.Thread(target=_worker, daemon=True).start()

    @mainthread
    def update_results(self, label, conf, nutri_data, recipes):
        text = f"Looks like {label} ({conf*100:.1f}% sure).

"
        if nutri_data and nutri_data.get("foods"):
            f = nutri_data["foods"][0]
            text += f"🔥 Calories: {f.get('nf_calories')} kcal\n"
            text += f"💪 Protein: {f.get('nf_protein')}g, 🍝 Carbs: {f.get('nf_total_carbohydrate')}g, 🥑 Fat: {f.get('nf_total_fat')}g\n\n"
        else:
            text += "No nutrition data. Did your phone brain fry?\n\n"
        if recipes:
            text += "Recipes to satisfy your savage hunger:\n"
            for r in recipes:
                text += f"• {r['label']} ({r['calories']} kcal) – {r['url']}\n"
        else:
            text += "No recipes found. Are you sure that’s edible?\n"
        self.ids.result_label.text = text

    @mainthread
    def show_error(self, msg):
        MDDialog(title="Error 😭", text=msg, size_hint=(0.8, 0.4)).open()

class RootScreenManager(ScreenManager):
    pass

class FoodSnapApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        self.classifier = FoodClassifier(
            model_path=os.path.join(self.user_data_dir, "model.tflite"),
            labels_path=os.path.join(self.user_data_dir, "labels.txt")
        )
        self.copy_assets()
        sm = RootScreenManager()
        sm.add_widget(MainScreen(name="main"))
        return sm

    def copy_assets(self):
        import shutil
        base = self.directory
        dest_model = os.path.join(self.user_data_dir, "model.tflite")
        dest_labels = os.path.join(self.user_data_dir, "labels.txt")
        if not os.path.exists(dest_model):
            shutil.copy(os.path.join(base, "app/assets/model.tflite"), dest_model)
        if not os.path.exists(dest_labels):
            shutil.copy(os.path.join(base, "app/assets/labels.txt"), dest_labels)

    def on_start(self):
        pass
