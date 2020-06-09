import aber_past_paper_retriever
import tkinter
from tkinter import ttk, filedialog, messagebox

class App(object):

    def __init__(self):
        self.retriever = aber_past_paper_retriever.PaperRetriever()
        
        self.root = tkinter.Tk()
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('Aber Uni Past Paper Retriever')

        frm = ttk.Frame(self.root)
        frm.pack(expand=True, fill='both')
        
        # username field
        ttk.Label(frm, text='Aber Username').grid(row=2, column=1, padx=10, pady=8)
        self.username_field = ttk.Entry(frm, show='*')
        self.username_field.grid(row=2, column=2, padx=10, pady=8)
        
        # password field
        ttk.Label(frm, text='Aber Password').grid(row=3, column=1, padx=10, pady=8)
        self.password_field = ttk.Entry(frm, show='*')
        self.password_field.grid(row=3, column=2, padx=10, pady=8)
        
        # horizontal divider
        ttk.Separator(frm).grid(row=4, column=1, columnspan=2, padx=10, pady=8, ipadx=160)
        
        # graduate level dropdown
        graduate_level_options = ['Undergraduate', 'Postgraduate']
        ttk.Label(frm, text='Graduate Level').grid(row=5, column=1, padx=10, pady=8)
        self.graduate_level_combo = ttk.Combobox(frm, values=graduate_level_options, state='readonly', width=65)
        self.graduate_level_combo.grid(row=5, column=2, padx=10, pady=8)
        # bind graduate level dropdown
        self.graduate_level_combo.bind('<<ComboboxSelected>>', self.get_department_values)
        
        # department dropdown
        ttk.Label(frm, text='Department').grid(row=6, column=1, padx=10, pady=8)
        self.department_combo = ttk.Combobox(frm, values=[], state='disabled', width=65)
        self.department_combo.grid(row=6, column=2, padx=10, pady=8)
        self.department_combo.bind('<<ComboboxSelected>>', self.departmentCallback)
        
        # module dropdown
        ttk.Label(frm, text='Module').grid(row=7, column=1, padx=10, pady=8)
        self.module_field = ttk.Entry(frm, state='disabled', width=65)
        self.module_field.grid(row=7, column=2, padx=10, pady=8)
        
        # directory select button
        ttk.Label(frm, text='Choose Destination Folder').grid(row=8, column=1, padx=10, pady=8)
        self.destination_directory_button = ttk.Button(frm, text='Select Folder', command=self.selectFolderCallback)
        self.destination_directory_button.grid(row=8, column=2, padx=10, pady=8)
        
        # horizontal divider
        ttk.Separator(frm).grid(row=9, column=1, columnspan=2, padx=10, pady=8, ipadx=160)
        
        # submit form button
        self.submit_form_button = ttk.Button(frm, text='Request Papers', state='disabled', command=self.submitFormCallback)
        self.submit_form_button.grid(row=10, column=1, columnspan=2, padx=10, pady=8)


    def get_department_values(self, eventObject):
        self.department_dict = self.retriever.get_departments()
        new_values = list(self.department_dict.keys())
        self.update_department_values_combo(new_values)

    def update_department_values_combo(self, new_values):
        self.department_combo['values'] = new_values
        self.department_combo['state'] = 'readonly'

    def departmentCallback(self, eventObject):
        graduate_level = self.graduate_level_combo.get()
        self.retriever.set_graduate_level(graduate_level)
        department_name = self.department_combo.get()
        department_url = self.department_dict.get(department_name)
        self.retriever.set_department_url(department_url)
        # enable module field
        self.module_field['state'] = 'normal'
        
    def validateModuleField(self):
        module_field_content = self.module_field.get()
      
        try:
            self.retriever.set_module_code(module_field_content)
        except ValueError:
            messagebox.showerror('Error', 'Invalid Module Code Provided - does not match "two letters five numbers" OR "three letters four numbers" format')
            # disable submit button
            self.submit_form_button['state'] = 'disabled'

    def selectFolderCallback(self):
        self.destination_directory_path = filedialog.askdirectory()

        # check directory selected
        if (not self.destination_directory_path is None) and (not self.module_field.get() is None):
            # set output destination
            self.retriever.set_destination_folder(self.destination_directory_path)
            # enable submit button
            self.submit_form_button['state'] = 'normal'

    def submitFormCallback(self):
        # TODO: this
        
        self.validateModuleField()
        
        # set credentials
        self.retriever.set_auth_header(self.username_field.get(), self.password_field.get())
        
        self.retriever.move_into_module_folder()
        
        retrieved_message = self.retriever.retrieve()
        messagebox.showinfo('Information', retrieved_message)
        
        self.retriever.move_out_of_module_folder()
