import pyperclip
import time
from fpdf import FPDF
import subprocess
import threading
import keyboard
import re
import clipboard
import pyautogui
import threading
import queue
cmd_queue = queue.Queue()
### run pip install -r requirements.txt to auto install the stuff
#i made this like a year before i put this on github and low key i forgot what i did how i did it.
#i like Aria english at fast speed and it should auto create a pdf and sometimes starts it. even if you never started edge itll start edge for you.

PDF_PATH = "C:/temp/temp_voice_reader.pdf"
EDGE_PATH = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"


print("---- Usage Guide ----")
print("Ctrl+Alt+Shift+R: Open clipboard content as a PDF in Edge and activate reader mode.")
print("Ctrl+Alt+Shift+F: Clean and format the clipboard content, then create a PDF.")
print("---------------------")
print("PSA YOU FORGET SHIT, copy something for this script to start\n then f to format and r to read")
print("dont fprget to love yourself <3")

def command_worker():
    while True:
        # Block until a command is available
        cmd = cmd_queue.get()
        if cmd == "open_pdf":
            open_pdf_in_edge()
        elif cmd == "sentence_fixer":
            sentence_fragment_fixer()
            print("prepped for ripping")
        elif cmd == "pokemon_list_fixer":  # Add this block to handle the pokemon list formatting
            pokemon_list_fixer()
            print("Formatted Pokemon list")
        # Signal the task is done
        cmd_queue.task_done()

def enqueue_command(command):
    if command not in list(cmd_queue.queue):
        cmd_queue.put(command)

def hotkey_listener():
    keyboard.add_hotkey('ctrl+alt+shift+r', enqueue_command, args=["open_pdf"])
    keyboard.add_hotkey('ctrl+alt+shift+f', enqueue_command, args=["sentence_fixer"])
    keyboard.add_hotkey('ctrl+alt+shift+h', enqueue_command, args=["pokemon_list_fixer"])
    
    # Keep the script running
    keyboard.wait()


        
def open_pdf_in_edge():
    global live_cb
    cb_check = pyperclip.paste()
    if cb_check != live_cb:
        print("New clipboard data")
        create_pdf(cb_check)
        live_cb = cb_check
    else:
        print("No new clipboard data")
    subprocess.Popen([EDGE_PATH, PDF_PATH])
    time.sleep(0.5)  # Wait for Edge to open
    #activate_edge_reader()
    pyautogui.hotkey("ctrl", "shift", "u")
    print("activated edge reader")

      
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('Meiryo', '', 'C:/Windows/Fonts/meiryo.ttc')
    pdf.set_font("Meiryo", size=12)
    pdf.multi_cell(0, 7, data)
    pdf.output(PDF_PATH)
    print("Created PDF")

def sentence_fragment_fixer():
    global live_cb
    live_cb = pyperclip.paste()
    cln_cb = clean_clipboard(live_cb)
    cln_cb = re.sub(r'\s+', ' ', cln_cb)
    cln_cb = re.sub(r'([.?!]) ', r'\1\n', cln_cb)
    cln_cb = re.sub(r'\n.\n', '\n', cln_cb)
    cln_cb = re.sub(r'\n\ .\n', '\n', cln_cb)
    cln_cb = re.sub(r'\n\ .\n', '\n', cln_cb)
    cln_cb = re.sub(r'\n.\n', '\n', cln_cb)
    cln_cb = re.sub(r'\n ', '\n', cln_cb)    
    cln_cb = re.sub(r'^\s+|\s+$', '', cln_cb)
    pyperclip.copy(cln_cb)
    live_cb = pyperclip.paste()
    create_pdf(cln_cb)


def pokemon_list_fixer():
    global live_cb
    live_cb = pyperclip.paste()
    formatted_data = reformat_pokemon_list(live_cb)
    pyperclip.copy(formatted_data)
    live_cb = pyperclip.paste()
    create_pdf(formatted_data)

def reformat_pokemon_list(data):
    pattern = r'(#\d{4} [^#\n]+? [^\s]+)(?= #|\Z)'
    formatted_data = re.sub(pattern, r'\1\n', data)
    return formatted_data
    
def clean_clipboard(clipboard_data):
    cleaned_text = clipboard_data.strip()
    cleaned_text = rm_garbage_data1(cleaned_text)

    clipboard.copy(cleaned_text)
    print(f"{cleaned_text}")
    return cleaned_text

def rm_garbage_data1(data):
    unwanted_strings = [
        "Press [CTRL + S] to save as a note (Required)",
        ": Added to Selection",
        "Press [CTRL + S] to save as a note",
        "(Required)",
        "[SOUND]",
        "[MUSIC]",
        "Interactive Transcript - Enable basic transcript mode by pressing the escape key",
        "You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S.",
        "To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key.",
        "For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys.",
        "Some screen readers may require using CTRL in conjunction with the alt key"
    ]
    for unwanted_string in unwanted_strings:
        data = data.replace(unwanted_string, "")
    
    # Remove patterns of periods followed by multiple spaces
    data = re.sub(r' \.(\s*​\.)*\s*', '', data)
    pyperclip.copy(data)
    return data


live_cb = pyperclip.paste()
create_pdf(live_cb)
# Start the command worker thread
threading.Thread(target=command_worker, daemon=True).start()

# Call hotkey_listener directly
hotkey_listener()
