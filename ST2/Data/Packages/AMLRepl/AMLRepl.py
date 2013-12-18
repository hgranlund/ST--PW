import sublime
import sublime_plugin
import subprocess
import sys
import time
import webbrowser
from threading import Thread


aml_manual_path = ""
aml_start_path = ""
aml_batch_file = ""

repl_process = None
output_lines = []
output_view = None

class AmlReplCommand(sublime_plugin.TextCommand):

    def PrintStdout(self, edit, process):
        global output_lines

        while process.poll() is None:
            output = process.stdout.readline()
            output_lines.append(output)

    def run(self, edit):
        self.view.set_name("AML REPL")
        self.view.set_syntax_file("Packages/AML/Aml.tmLanguage")

        global aml_manual_path, aml_start_path, aml_batch_file
        settings = sublime.load_settings("AMLRepl.sublime-settings")
        aml_manual_path = settings.get("aml_manual_path")
        aml_start_path = settings.get("aml_start_path")
        aml_batch_file = settings.get("aml_batch_file")

        global repl_process
        repl_process = subprocess.Popen(aml_batch_file, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=aml_start_path)

        global output_view
        output_view = self.view

        stdout_thread = Thread(target=self.PrintStdout, args=[edit, repl_process])
        stdout_thread.setDaemon(True)
        stdout_thread.start()

        counter = 0
        while (not 'nil\r\n' in output_lines) and counter < 100:
            time.sleep(0.1)
            counter += 1

        self.view.run_command('output_lines')


class WindowEventCommand(sublime_plugin.EventListener):

    def on_close(self, view):
        global repl_process

        if repl_process:
            repl_process.stdin.write("(quit)\n")
            repl_process.terminate()
            repl_process = NoneF

class ReplQuitCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global repl_process

        if repl_process:
            output_view.run_command('output_lines')
            repl_process.stdin.write("(quit)\n")
            repl_process.terminate()
            repl_process = None
            output_view.insert(edit, output_view.size(), "AML process terminated. Bye :-)")


class ReplEvalCommand(sublime_plugin.TextCommand):

    def last_sexp(self, string):
        sexp, bracet_count, bracket_match, done  = "", 0, 0, 0

        for c in reversed(string):
            if c == ')':
                bracket_match += 1
                bracet_count += 1

            elif c == '(':
                bracket_match -= 1
                bracet_count += 1

            if done == 0 and bracet_count > 0 :
                sexp = c + sexp
            
            elif done == 1 and c == '\'':
                sexp = c + sexp
            
            elif done > 1:
                break

            if bracet_count > 1 and bracket_match == 0:
                done += 1

        return sexp

    def run(self, edit):
        global repl_process

        if repl_process:
            input_substr = None
            position = self.view.sel()[0]

            if position.begin() == position.end():
                input_substr = self.last_sexp(self.view.substr(sublime.Region(0, self.view.size())))
            else:
                input_substr = self.view.substr(sublime.Region(position.begin(), position.end()))  

            output_view.insert(edit, self.view.size(), "\n")
            repl_process.stdin.write("%s\n" % input_substr)
  
            output_view.run_command('output_lines')
        else:
            output_view.insert(edit, output_view.size(), "No AML process initialized. Please restart AMLRepl.\n")

class FileEvalCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global repl_process
        global output_view

        if repl_process:
            input_substr = self.view.substr(sublime.Region(0, self.view.size()))
            repl_process.stdin.write("%s\n" % input_substr)
            output_view.run_command('output_lines')
        else:
            output_view.insert(edit, self.view.size(), "No AML process initialized. Please restart AMLRepl.\n")

class OutputLinesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global output_lines
        counter = 0

        while output_lines == [] and counter < 10:
            time.sleep(0.1)
            counter += 1

        for line in output_lines:
            self.view.insert(edit, self.view.size(), line)

        self.view.run_command("goto_line", {"line": self.view.size()})
        output_lines = []

class AmlReferenceManualCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global aml_manual_path
        
        url = "file:///" + aml_manual_path + "index.html"
        webbrowser.open_new(url)

class AmlGuiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if repl_process:
            output_view.insert(edit, self.view.size(), "\n")
            repl_process.stdin.write("%s\n" % "(aml)")
  
            output_view.run_command('output_lines')
        else:
            output_view.insert(edit, output_view.size(), "No AML process initialized. Please restart AMLRepl.\n")

class AunitGuiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if repl_process:
            output_view.insert(edit, self.view.size(), "\n")

            repl_process.stdin.write("%s\n" % "(compile-system :aunit-core-system)") 
            output_view.run_command('output_lines')
            repl_process.stdin.write("%s\n" % "(compile-system :aunit-print-system)") 
            output_view.run_command('output_lines')
            repl_process.stdin.write("%s\n" % "(compile-system :aunit-gui-system)") 
            output_view.run_command('output_lines')
            repl_process.stdin.write("%s\n" % "(compile-system :aunit-main-system)") 
            output_view.run_command('output_lines')
            
            repl_process.stdin.write("%s\n" % "(aunit)") 
            output_view.run_command('output_lines')
        else:
            output_view.insert(edit, output_view.size(), "No AML process initialized. Please restart AMLRepl.\n")