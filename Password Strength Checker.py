import tkinter as tk
from tkinter import ttk
import re

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))
        
        # Create main frame
        main_frame = ttk.Frame(root, padding=20)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Strength Checker", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Password entry
        ttk.Label(main_frame, text="Enter Password:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="•", width=30)
        self.password_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.password_var.trace_add("write", self.check_password_strength)
        
        # Show password checkbox
        self.show_password_var = tk.IntVar()
        show_password_cb = ttk.Checkbutton(main_frame, text="Show password", variable=self.show_password_var,
                                          command=self.toggle_password_visibility)
        show_password_cb.grid(row=3, column=0, sticky=tk.W, pady=(0, 20))
        
        # Strength indicator
        ttk.Label(main_frame, text="Strength:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.strength_label = ttk.Label(main_frame, text="None", font=("Arial", 12, "bold"))
        self.strength_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Criteria frame
        criteria_frame = ttk.LabelFrame(main_frame, text="Password Criteria", padding=10)
        criteria_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Criteria labels
        self.length_label = ttk.Label(criteria_frame, text="✓ At least 8 characters")
        self.length_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.upper_label = ttk.Label(criteria_frame, text="✓ Contains uppercase letters (A-Z)")
        self.upper_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.lower_label = ttk.Label(criteria_frame, text="✓ Contains lowercase letters (a-z)")
        self.lower_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.number_label = ttk.Label(criteria_frame, text="✓ Contains numbers (0-9)")
        self.number_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.special_label = ttk.Label(criteria_frame, text="✓ Contains special characters (!@#$%^&*)")
        self.special_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        # Suggestions
        ttk.Label(main_frame, text="Suggestions:").grid(row=8, column=0, sticky=tk.W, pady=(0, 5))
        self.suggestion_text = tk.Text(main_frame, height=4, width=50, font=("Arial", 10), bg="#f0f0f0")
        self.suggestion_text.grid(row=9, column=0, sticky=(tk.W, tk.E))
        self.suggestion_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Initial update
        self.update_criteria_indicators("")
    
    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def check_password_strength(self, *args):
        password = self.password_var.get()
        strength = 0
        suggestions = []
        
        # Check length
        has_length = len(password) >= 8
        if has_length:
            strength += 20
        else:
            suggestions.append("Add more characters to make at least 8")
        
        # Check uppercase
        has_upper = bool(re.search(r'[A-Z]', password))
        if has_upper:
            strength += 20
        else:
            suggestions.append("Include uppercase letters (A-Z)")
        
        # Check lowercase
        has_lower = bool(re.search(r'[a-z]', password))
        if has_lower:
            strength += 20
        else:
            suggestions.append("Include lowercase letters (a-z)")
        
        # Check numbers
        has_number = bool(re.search(r'[0-9]', password))
        if has_number:
            strength += 20
        else:
            suggestions.append("Include numbers (0-9)")
        
        # Check special characters
        has_special = bool(re.search(r'[!@#$%^&*]', password))
        if has_special:
            strength += 20
        else:
            suggestions.append("Include special characters (!@#$%^&*)")
        
        # Update progress bar and strength label
        self.progress['value'] = strength
        
        if strength < 40:
            strength_text = "Weak ❌"
            color = "red"
        elif strength < 80:
            strength_text = "Medium ⚠️"
            color = "orange"
        else:
            strength_text = "Strong ✅"
            color = "green"
        
        self.strength_label.config(text=strength_text, foreground=color)
        
        # Update criteria indicators
        self.update_criteria_indicators(password)
        
        # Update suggestions
        self.suggestion_text.config(state=tk.NORMAL)
        self.suggestion_text.delete(1.0, tk.END)
        if suggestions:
            self.suggestion_text.insert(tk.END, "To improve your password:\n")
            for i, suggestion in enumerate(suggestions, 1):
                self.suggestion_text.insert(tk.END, f"{i}. {suggestion}\n")
        else:
            self.suggestion_text.insert(tk.END, "Your password meets all criteria! ✅")
        self.suggestion_text.config(state=tk.DISABLED)
    
    def update_criteria_indicators(self, password):
        # Update each criteria indicator based on whether it's met
        criteria = [
            (len(password) >= 8, self.length_label),
            (bool(re.search(r'[A-Z]', password)), self.upper_label),
            (bool(re.search(r'[a-z]', password)), self.lower_label),
            (bool(re.search(r'[0-9]', password)), self.number_label),
            (bool(re.search(r'[!@#$%^&*]', password)), self.special_label)
        ]
        
        for condition, label in criteria:
            if condition:
                label.config(foreground="green")
            else:
                label.config(foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()