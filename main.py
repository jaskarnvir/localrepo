import os
import re
from tkinter import *
from PIL import ImageTk, Image
from num2words import num2words

import check_internet
import database
import db_credentials
import deepa_autoz_database
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
from tkinter import ttk, messagebox
from tkinter import filedialog
from ctypes import windll
import ctypes
import copy
import threading

import error_notifier


# n
class Main:
    def __init__(self):
        self.back_temp = None
        self.redispatch_amount_var = None
        self.windows = "closed"
        self.pending_window = False # for checking if window already opened

    def window(self,data=None, all_data=None, listener=None, work_data=None):
        self.listener = listener
        self.data = data
        # print(f"data ------- {self.data}\n\n")
        self.all_data = all_data
        self.work_data = work_data
        self.pending_data = self.data[0]["pending_document"]
        windll.shcore.SetProcessDpiAwareness(2)
        self.main_root = Tk()
        # self.main_root.wm_attributes("-toolwindow", 1)

        self.main_root.configure(bg='#B39CD0')
        self.color_1 = "#ffffff"
        self.bg_color = "#B39CD0"
        self.screen_width = self.main_root.winfo_screenwidth()
        self.screen_height = self.main_root.winfo_screenheight()
        window_width = self.main_root.winfo_width()
        window_height = self.main_root.winfo_height()
        hdc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 corresponds to LOGPIXELSX
        ctypes.windll.user32.ReleaseDC(0, hdc)
        standard_dpi = 96
        screen_scale_factor = dpi / standard_dpi
        # print(f"Display Size: {window_width}x{window_height} pixels")
        # print(f"Display DPI: {dpi} DPI")
        # print(f"Display Scale Factor: {screen_scale_factor}")

        if dpi == 96 and screen_scale_factor == 1.0:
            self.entry_font_size = 15
            self.date_entry_size = 15
            self.font_size = "16"
            self.field_width = 19
            self.field_width2 = 8
            self.field_width_2 = 14
            self.combobox_size = 12
            self.combobox_width = 11
            self.label_size = 13


        elif dpi == 144 and screen_scale_factor == 1.5:
            self.entry_font_size = 10
            self.date_entry_size = 11
            self.font_size = "11"
            self.field_width = 19
            self.field_width2 = 8
            self.field_width_2 = 14
            self.combobox_size = 8
            self.combobox_width = 10
            self.label_size = 9

        self.main_root.title("Car Cue")
        self.icon = ImageTk.PhotoImage(Image.open(r"images\carcue.ico"))
        self.main_root.iconphoto(True,self.icon)
        self.app_width = 1920
        self.app_height = 1032
        self.screen_width = self.main_root.winfo_screenwidth()
        self.screen_height = self.main_root.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.app_width / 2)
        self.y = (self.screen_height / 2) - (self.app_height / 2 + 28)
        self.main_root.geometry(f"{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}")
        # self.main_root.resizable(False, False)
        self.main_root.maxsize(1920, 1032)
        self.image = Image.open(r"images\all_work_img\all_work_bg_commercial.png")
        self.photo = ImageTk.PhotoImage(image=self.image)
        self.img_lbl = Label(self.main_root, image=self.photo)
        self.img_lbl.place(x=-2, y=0)

        self.back_btn_img = ImageTk.PhotoImage(Image.open(r"images\back_btn.png"))
        self.back_btn_btn = Button(self.main_root,
                                   text="open file",
                                   font=(None, 12),
                                   image=self.back_btn_img,
                                   background="black",
                                   borderwidth=0,
                                   activebackground="black",
                                   relief=FLAT,
                                   command=self.back_but_fun,
                                   )
        self.back_btn_btn.place(x=10, y=10)
        self.pending_btn_img = ImageTk.PhotoImage(Image.open(r"images\pending_button.png"))
        self.pending_data_btn = Button(self.main_root,
                                       # text="PENDING DOCUMENT",
                                       image=self.pending_btn_img,
                                       borderwidth=0,
                                       # width=150,
                                       # height=35,
                                       bg="black",
                                       activebackground="black",
                                       relief=FLAT,
                                       command=self.pending_doc_win)
        self.pending_data_btn.place(x=65, y=10)

        self.payment_top_level_open = False
        self.payment_top_level = None

        self.payment_btn_img = ImageTk.PhotoImage(Image.open(r"images\payment_entry_button.png"))
        self.payment_entry_btn = Button(text="Payment entry", image=self.payment_btn_img,
                                        borderwidth=0,
                                        bg="#b39cd0",
                                        activebackground="#b39cd0",
                                        command=self.payment_entry_win
                                        )
        self.payment_entry_btn.place(x=1392, y=71)


        self.total_amount_var = StringVar()
        self.total_amount_var.set(self.data[0]["total_amount"])
        self.total_amount_entry = Entry(textvariable=self.total_amount_var,
                                        bg=self.color_1,
                                        state="readonly",
                                        readonlybackground="#B39CD0",
                                        disabledbackground="#B39CD0",
                                        validate="key",
                                        validatecommand=(self.main_root.register(self.validate_amount),
                                                         "%S"),
                                        # border=0,
                                        width=17,
                                        font=("Helvetica", self.entry_font_size, "bold"))
        self.total_amount_entry.place(x=1685, y=67)

        self.recieved_amount_var = StringVar()
        self.recieved_amount_entry = Entry(textvariable=self.recieved_amount_var,
                                           bg=self.color_1,
                                           state="readonly",
                                           readonlybackground="#B39CD0",
                                           disabledbackground="#B39CD0",
                                           validate="key",
                                           validatecommand=(self.main_root.register(self.validate_amount),
                                                            "%S"),
                                           # border=0,
                                           width=17,
                                           font=("Helvetica", self.entry_font_size, "bold"))
        self.recieved_amount_entry.place(x=1685, y=93)
        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
        # self.recieved_amount_var.set(self.data[0]["recieved_amount"])

        # self.recieved_amount_var.trace_add("write", self.pending_total)

        self.due_amount_var = StringVar()
        self.due_amount_entry = Entry(textvariable=self.due_amount_var,
                                      bg=self.color_1,
                                      state="readonly",
                                      readonlybackground="#B39CD0",
                                      disabledbackground="#B39CD0",
                                      validate="key",
                                      validatecommand=(self.main_root.register(self.validate_amount),
                                                       "%S"),
                                      # border=0,
                                      width=17,
                                      font=("Helvetica", self.entry_font_size, "bold"))
        self.due_amount_entry.place(x=1685, y=119)
        self.due_amount_var.set(self.data[0]["due_amount"])





        self.pending_status_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\status_pending.png"))
        self.completed_status_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\status_completed.png"))

        self.new1 = ImageTk.PhotoImage(Image.open(r"images\com_car_1.png"))
        self.new2 = ImageTk.PhotoImage(Image.open(r"images\pvt_car_1.png"))


        self.new1_1 = ImageTk.PhotoImage(Image.open(r"images\com_car_2.png"))
        self.new2_2 = ImageTk.PhotoImage(Image.open(r"images\pvt_car_2.png"))


        self.b1 = Button(image=self.new1_1, bg="black", borderwidth=0, activebackground="black",
                         command=self.a,
                         )
        self.b1.place(x=125, y=8)
        self.b2 = Button(image=self.new2, bg="black", borderwidth=0, activebackground="black",
                         command=self.b,
                         )
        self.b2.place(x=235, y=8)

        self.vehicle_type = StringVar()
        self.vehicle_type.set(data[0]["vehicle_type"])
        if self.vehicle_type.get() == "private":
            self.b()
        elif self.vehicle_type.get() == "commercial":
            self.a()

        self.edit_btn_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\edit_btn.png"))
        self.edit_data_btn = Button(self.main_root,
                                       # text="PENDING DOCUMENT",
                                       image=self.edit_btn_img,
                                       borderwidth=0,
                                       bg="#b39cd0",
                                       activebackground="#b39cd0",
                                       relief=FLAT,
                                       command=self.edit_vehicle_data
                                    )
        self.edit_data_btn.place(x=65, y=170)

        self.editing_done_btn_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\edit_done_btn.png"))
        self.editing_done_data_btn = Button(self.main_root,
                                       # text="PENDING DOCUMENT",
                                       image=self.editing_done_btn_img,
                                       borderwidth=0,
                                       bg="#b39cd0",
                                       activebackground="#b39cd0",
                                       relief=FLAT,
                                       command=self.edit_vehicle_done_data
                                    )

        self.name_var = StringVar()
        self.name_entry = Entry(textvariable=self.name_var,
                                state="readonly",
                                readonlybackground="white",
                                validate="key",
                                validatecommand=(self.main_root.register(self.validate_name), "%P"),
                                width=self.field_width,
                                border=0,
                                font=("Helvetica", self.font_size))
        self.name_entry.place(x=75, y=212)
        self.name_entry.bind('<KeyRelease>', lambda event: self.convert_name_to_uppercase())
        self.name_var.set(data[0]["name"])


        self.numberplate_no_var = StringVar()
        self.numberplate_no_entry = Entry(textvariable=self.numberplate_no_var,
                                          state="readonly",
                                          readonlybackground="white",
                                          bg=self.color_1,
                                          border=0,
                                          validate="key",
                                          validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                          width=self.field_width,
                                          font=("Helvetica", self.font_size))
        self.numberplate_no_entry.place(x=382, y=212)
        self.numberplate_no_entry.bind('<KeyRelease>', lambda event: self.convert_numberplate_to_uppercase())
        self.numberplate_no_var.set(data[0]["vehicle_no"])

        self.car_model_var = StringVar()
        self.car_model_entry = Entry(textvariable=self.car_model_var,
                                     state="readonly",
                                     readonlybackground="white",
                                     validate="key",
                                     validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                     width=self.field_width,
                                     bg=self.color_1,
                                     border=0,
                                     font=("Helvetica", self.font_size))
        self.car_model_entry.place(x=689, y=212)
        self.car_model_entry.bind('<KeyRelease>', lambda event: self.convert_car_model_to_uppercase())
        self.car_model_var.set(data[0]["vehicle_model"])

        self.engine_var = StringVar()
        self.engine_entry = Entry(textvariable=self.engine_var,
                                  state="readonly",
                                  readonlybackground="white",
                                  validate="key",
                                  validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                  width=self.field_width,
                                  bg=self.color_1, border=0, font=("Helvetica", self.font_size))
        self.engine_entry.place(x=996, y=212)
        self.engine_entry.bind('<KeyRelease>', lambda event: self.convert_engine_no_to_uppercase())
        self.engine_var.set(data[0]["engine_no"])

        self.chassis_no_var = StringVar()
        self.chassis_no_entry = Entry(textvariable=self.chassis_no_var,
                                      state="readonly",
                                      readonlybackground="white",
                                      validate="key",
                                      validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                      width=self.field_width,
                                      bg=self.color_1, border=0, font=("Helvetica", self.font_size))
        self.chassis_no_entry.place(x=1303, y=212)
        self.chassis_no_entry.bind('<KeyRelease>', lambda event: self.convert_chassis_no_to_uppercase())
        self.chassis_no_var.set(data[0]["chassis_no"])

        self.ph_no_var = StringVar()
        self.ph_no_entry = Entry(textvariable=self.ph_no_var,
                                 state="readonly",
                                 readonlybackground="white",
                                 validate="key",
                                 validatecommand=(self.main_root.register(self.validate_phone), "%P"),
                                 width=self.field_width,
                                 bg=self.color_1, border=0, font=("Helvetica", self.font_size))
        self.ph_no_entry.place(x=1610, y=212)
        self.ph_no_var.set(data[0]["ph_no"])

        # =======================================1ST ROW==============================================
        # self.rc_redispatch_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_redispatch.png"))
        rc_redispatch_button = Button(text="   RC REDISPATCH   ",font=("Helvetica", 20,"bold"),
                                      # image=self.rc_redispatch_img,
                                      # borderwidth=0,
                                      bg=self.bg_color,
                                      activebackground=self.bg_color,
                                      command=self.open_redispatch_win)
        rc_redispatch_button.grid(row=0, column=0, pady=0, padx=40, rowspan=4)
        self.redispatch_top_level_open = False
        self.redispatch_top_level = None


        # self.rc_duplicate_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_duplicate.png"))
        rc_duplicate_button = Button(text="  RC DUPLICATE  ", font=("Helvetica", 20, "bold"),
                                     # image=self.rc_duplicate_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_rc_duplicate_win,
                                     )
        rc_duplicate_button.grid(row=0, column=1,pady=170, padx=30, rowspan=4)
        self.rc_duplicate_top_level_open = False
        self.rc_duplicate_top_level = None

        # self.rc_modify_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_modify.png"))
        rc_modify_button = Button(text="     RC MODIFY     ",font=("Helvetica", 20, "bold"),
                                  # image=self.rc_modify_img,
                                  # borderwidth=0,
                                  bg=self.bg_color,
                                  activebackground=self.bg_color,
                                  command=self.open_rc_modify_win
                                  )
        rc_modify_button.grid(row=0, column=2,pady=170, padx=30, rowspan=4)
        self.rc_modify_top_level_open = False
        self.rc_modify_top_level = None

        # self.rc_transfer_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_transfer.png"))
        rc_transfer_button = Button(text="  RC TRANSFER  ",font=("Helvetica", 20, "bold"),
                                    # image=self.rc_transfer_img,
                                    # borderwidth=0,
                                    bg=self.bg_color,
                                    activebackground=self.bg_color,
                                    command=self.open_rc_transfer_win,
                                    )
        rc_transfer_button.grid(row=0, column=4,pady=170, padx=30, rowspan=4)
        self.rc_transfer_top_level_open = False
        self.rc_transfer_top_level = None

        # self.rc_conversion_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_conversion.png"))
        rc_conversion_button = Button(text="RC CONVERSION",font=("Helvetica", 20, "bold"),
                                      # image=self.rc_conversion_img,
                                      # borderwidth=0,
                                      bg=self.bg_color,
                                      activebackground=self.bg_color,
                                      command=self.open_rc_conversion_win,
                                      )
        rc_conversion_button.grid(row=0, column=5,pady=170, padx=30, rowspan=4)
        self.rc_conversion_top_level_open = False
        self.rc_conversion_top_level = None


        # extra label to set gui interface
        Label(bg=self.bg_color,font=(None,1)).grid(row=0, column=6,pady=190, padx=30 )
        # Label(text=".",foreground="#3b0085",bg="#b39cd0",font=(None,1)).grid(row=0, column=5,pady=185, padx=30 )









        # =======================================2ND ROW==============================================
        # self.hp_cancel_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\hp_cancel.png"))
        hp_cancel_button = Button(text="        HP CANCEL       ",font=("Helvetica", 20, "bold"),
                                  # image=self.hp_cancel_img,
                                  # borderwidth=0,
                                  bg=self.bg_color,
                                  activebackground=self.bg_color,
                                  command=self.open_hp_cancel_win
                                  )
        hp_cancel_button.grid(row=1, column=0, padx=30)
        self.hp_cancel_top_level_open = False
        self.hp_cancel_top_level = None

        # self.hp_made_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\hp_made.png"))
        hp_made_button = Button(text="   HP MADE   ",font=("Helvetica", 20, "bold"),
                                # image=self.hp_made_img,
                                # borderwidth=0,
                                bg=self.bg_color,
                                activebackground=self.bg_color,
                                command=self.open_hp_made_win
                                )
        hp_made_button.grid(row=1, column=1, padx=30)
        self.hp_made_top_level_open = False
        self.hp_made_top_level = None

        # self.hsrp_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\hsrp.png"))
        hsrp_button = Button(text="   HSRP   ",font=("Helvetica", 20, "bold"),
                             # image=self.hsrp_img,
                             # borderwidth=0,
                             bg=self.bg_color,
                             activebackground=self.bg_color,
                             command=self.open_hsrp_win
                             )
        hsrp_button.grid(row=1, column=2, padx=30)
        self.hsrp_top_level_open = False
        self.hsrp_top_level = None

        # self.fitness_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\fitness.png"))
        fitness_button = Button(text="FITNESS", font=("Helvetica", 20, "bold"),
                                # image=self.fitness_img,
                                # borderwidth=0,
                                bg=self.bg_color,
                                activebackground=self.bg_color,
                                command=self.open_fitness_win
                                )
        fitness_button.grid(row=1, column=4, padx=30)
        self.fitness_top_level_open = False
        self.fitness_top_level = None

        # self.insurance_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\insurance.png"))
        insurance_button = Button(text="INSURANCE", font=("Helvetica", 20, "bold"),
                                  # image=self.insurance_img,
                                  # borderwidth=0,
                                  bg=self.bg_color,
                                  activebackground=self.bg_color,
                                  command=self.open_insurance_win
                                  )
        insurance_button.grid(row=1, column=5, padx=30)
        self.insurance_top_level_open = False
        self.insurance_top_level = None










        # =======================================3RD ROW==============================================
        # self.pb_late_fine_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\pb_late_fine.png"))
        pb_late_fine_button = Button(text="      PB LATE FINE     ", font=("Helvetica", 20, "bold"),
                                     # image=self.pb_late_fine_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_pb_late_fine_win
                                     )
        pb_late_fine_button.grid(row=2, column=0, pady=30, padx=30)
        self.pb_late_fine_top_level_open = False
        self.pb_late_fine_top_level = None

        # self.np_late_fine_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\np_late_fine.png"))
        np_late_fine_button = Button(text="NP LATE FINE", font=("Helvetica", 20, "bold"),
                                     # image=self.np_late_fine_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_np_late_fine_win
                                     )
        np_late_fine_button.grid(row=2, column=1,pady=30, padx=30)
        self.np_late_fine_top_level_open = False
        self.np_late_fine_top_level = None

        # self.pb_permit_new_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\pb_permit_new.png"))
        pb_permit_new_button = Button(text="PB PERMIT NEW", font=("Helvetica", 20, "bold"),
                                      # image=self.pb_permit_new_img,
                                      # borderwidth=0,
                                      bg=self.bg_color,
                                      activebackground=self.bg_color,
                                      command=self.open_pb_permit_new_win
                                      )
        pb_permit_new_button.grid(row=2, column=2,pady=30, padx=30)
        self.pb_permit_new_top_level_open = False
        self.pb_permit_new_top_level = None

        # self.np_permit_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\np_permit.png"))
        np_permit_button = Button(text="NP PERMIT", font=("Helvetica", 20, "bold"),
                                  # image=self.np_permit_img,
                                  # borderwidth=0,
                                  bg=self.bg_color,
                                  activebackground=self.bg_color,
                                  command=self.open_np_permit_win
                                  )
        np_permit_button.grid(row=2, column=4,pady=30, padx=30)
        self.np_permit_top_level_open = False
        self.np_permit_top_level = None

        # self.alteration_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\alteration.png"))
        alteration_button = Button(text="ALTERATION", font=("Helvetica", 20, "bold"),
                                   # image=self.alteration_img,
                                   # borderwidth=0,
                                   bg=self.bg_color,
                                   activebackground=self.bg_color,
                                   command=self.open_alteration_win
                                   )
        alteration_button.grid(row=2, column=5,pady=30, padx=30)
        self.alteration_top_level_open = False
        self.alteration_top_level = None







        # =======================================4TH ROW==============================================
        # self.tax_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\tax.png"))
        tax_button = Button(text="              TAX              ", font=("Helvetica", 20, "bold"),
                            # image=self.tax_img,
                            # borderwidth=0,
                            bg=self.bg_color,
                            activebackground=self.bg_color,
                            command=self.open_tax_win
                            )
        tax_button.grid(row=3, column=0,pady=0, padx=30)
        self.tax_top_level_open = False
        self.tax_top_level = None

        # self.tax_no_due_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\tax_no_due.png"))
        tax_no_due_button = Button(text="TAX NO DUE", font=("Helvetica", 20, "bold"),
                                   # image=self.tax_no_due_img,
                                   # borderwidth=0,
                                   bg=self.bg_color,
                                   activebackground=self.bg_color,
                                   command=self.open_tax_no_due_win
                                   )
        tax_no_due_button.grid(row=3, column=1,pady=0, padx=30)
        self.tax_no_due_top_level_open = False
        self.tax_no_due_top_level = None

        # self.reassignment_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\re_assignment.png"))
        reassignment_button = Button(text="RE-ASSIGNMENT",font=("Helvetica", 20, "bold"),
                                     # image=self.reassignment_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_reassignment_win
                                     )
        reassignment_button.grid(row=3, column=2,pady=0, padx=30)
        self.reassignment_top_level_open = False
        self.reassignment_top_level = None

        # self.noc_sent_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\noc_sent.png"))
        noc_sent_button = Button(text="NOC SENT", font=("Helvetica", 20, "bold"),
                            # image=self.noc_sent_img,
                            # borderwidth=0,
                            bg=self.bg_color,
                            activebackground=self.bg_color,
                            command=self.open_noc_sent_win
                            )
        noc_sent_button.grid(row=3, column=4,pady=0, padx=30)
        self.noc_sent_top_level_open = False
        self.noc_sent_top_level = None


        # self.noc_accept_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\noc_accept.png"))
        noc_accept_button = Button(text="NOC ACCEPT", font=("Helvetica", 20, "bold"),
                            # image=self.noc_accept_img,
                            # borderwidth=0,
                            bg=self.bg_color,
                            activebackground=self.bg_color,
                            command=self.open_noc_accept_win
                            )
        noc_accept_button.grid(row=3, column=5,pady=0, padx=30)
        self.noc_accept_top_level_open = False
        self.noc_accept_top_level = None











        # =======================================5TH ROW==============================================
        # self.pb_surrender_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\pb_surrender.png"))
        pb_surrender_button = Button(text="    PB SURRENDER   ", font=("Helvetica", 20, "bold"),
                                     # image=self.pb_surrender_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_pb_surrender_win
                                     )


        pb_surrender_button.grid(row=4, column=0,pady=30, padx=30)
        self.pb_surrender_top_level_open = False
        self.pb_surrender_top_level = None

        # self.np_surrender_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\np_surrender.png"))
        np_surrender_button = Button(text="NP SURRENDER",font=("Helvetica", 20, "bold"),
                                     # image=self.np_surrender_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_np_surrender_win
                                     )
        np_surrender_button.grid(row=4, column=1,pady=30, padx=30)
        self.np_surrender_top_level_open = False
        self.np_surrender_top_level = None

        # self.pollution_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\pollution.png"))
        pollution_button = Button(text="POLLUTION", font=("Helvetica", 20, "bold"),
                                  # image=self.pollution_img,
                                  # borderwidth=0,
                                  bg=self.bg_color,
                                  activebackground=self.bg_color,
                                  command=self.open_pollution_win
                                  )
        pollution_button.grid(row=4, column=2,pady=30, padx=30)
        self.pollution_top_level_open = False
        self.pollution_top_level = None

        # self.address_change_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\address_change.png"))
        address_change_button = Button(text="ADDRESS CHANGE", font=("Helvetica", 20, "bold"),
                                       # image=self.address_change_img,
                                       # borderwidth=0,
                                       bg=self.bg_color,
                                       activebackground=self.bg_color,
                                       command=self.open_address_change_win
                                       )
        address_change_button.grid(row=4, column=4,pady=30, padx=30)
        self.address_change_top_level_open = False
        self.address_change_top_level = None

        # self.fancy_number_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\fancy_number.png"))
        fancy_number_button = Button(text="FANCY NUMBER", font=("Helvetica", 20, "bold"),
                                     # image=self.fancy_number_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_fancy_number_win
                                     )
        fancy_number_button.grid(row=4, column=5,pady=30, padx=30)
        self.fancy_number_top_level_open = False
        self.fancy_number_top_level = None






        # =======================================6TH ROW==============================================
        # self.phone_change_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\phone_change.png"))
        phone_change_button = Button(text="PHONE NO. CHANGE", font=("Helvetica", 20, "bold"),
                                     # image=self.phone_change_img,
                                     # borderwidth=0,
                                     bg=self.bg_color,
                                     activebackground=self.bg_color,
                                     command=self.open_phone_change_win
                                     )
        phone_change_button.grid(row=5, column=0,pady=0, padx=30)
        self.phone_change_top_level_open = False
        self.phone_change_top_level = None


        # self.np_authorization_img= ImageTk.PhotoImage(Image.open(r"images\all_work_img\np_authorization.png"))
        np_authorization_button = Button(text="NP AUTHORIZATION", font=("Helvetica", 20, "bold"),
                                         # image=self.np_authorization_img,
                                         # borderwidth=0,
                                         bg=self.bg_color,
                                         activebackground=self.bg_color,
                                         command=self.open_np_authorization_win
                                         )
        np_authorization_button.grid(row=5, column=1,pady=0, padx=30)
        self.np_authorization_top_level_open = False
        self.np_authorization_top_level = None


        # self.rc_new_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_new.png"))
        rc_new_button = Button(text="RC NEW", font=("Helvetica", 20, "bold"),
                                      # image=self.rc_new_img,
                                      # borderwidth=0,
                                      bg=self.bg_color,
                                      activebackground=self.bg_color,
                                      command=self.open_rc_new_win
                               )
        rc_new_button.grid(row=5, column=2, pady=0, padx=30)
        self.rc_new_top_level_open = False
        self.rc_new_top_level = None


        # self.rc_renewal_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_renewal.png"))
        rc_renewal_button = Button(text="RC RENEWAL", font=("Helvetica", 20, "bold"),
                                      # image=self.rc_renewal_img,
                                      # borderwidth=0,
                                      bg=self.bg_color,
                                      activebackground=self.bg_color,
                                      command=self.open_rc_renewal_win
                                   )
        rc_renewal_button.grid(row=5, column=4, pady=0, padx=30)
        self.rc_renewal_top_level_open = False
        self.rc_renewal_top_level = None


        # self.new_registration_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\new_registration.png"))
        new_registration_button = Button(text="NEW REGISTRATION",font=("Helvetica", 20, "bold"),
                                         # image=self.new_registration_img,
                                      # borderwidth=0,
                                      bg=self.bg_color,
                                      activebackground=self.bg_color,
                                      command=self.open_new_registration_win
                                   )
        new_registration_button.grid(row=5, column=5, pady=0, padx=30)
        self.new_registration_top_level_open = False
        self.new_registration_top_level = None



        # =======================================7TH ROW==============================================
        # PHONE NO. CHANGE
        # NEW REGISTRATION
        #   OTHERS WORK
        # self.others_work_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\others_work.png"))
        others_work_button = Button(text="     OTHERS WORK    ", font=("Helvetica", 20, "bold"),
                                    # image=self.others_work_img,
                                    #   borderwidth=0,
                                      bg=self.bg_color,
                                      activebackground=self.bg_color,
                                      command=self.open_others_work_win
                                   )
        others_work_button.grid(row=6, column=0, pady=30, padx=30)
        self.others_work_top_level_open = False
        self.others_work_top_level = None



        # self.listener_thread = threading.Thread(target=self.close_listener)
        # self.main_root.protocol("WM_DELETE_WINDOW", self.on_close_)
        self.main_root.mainloop()


    # def on_close_(self):
    #     self.listener_thread.start()
    #     self.main_root.destroy()
    # def close_listener(self):
    #     self.listener.close()
    def update_data(self, all_data, new_data):
        print(f"---- {new_data}")
        for index, entry in enumerate(all_data):
            if entry['Id'] == new_data['Id']:
                all_data[index] = new_data
                break

    def edit_vehicle_data(self):
        """backup data fields so if data is didnot getting updated on database to revert changes in gui """
        self.back_temp = {}
        fields = {
            "name": self.name_var.get(),
            "vehicle_no": self.numberplate_no_var.get(),
            "vehicle_model": self.car_model_var.get(),
            "engine_no": self.engine_var.get(),
            "chassis_no": self.chassis_no_var.get(),
            "ph_no": self.ph_no_var.get(),
            "vehicle_type": self.vehicle_type.get()
        }

        for key, value in fields.items():
            self.back_temp[key] = value

        # enable all required fields
        self.name_entry.config(state="normal")
        self.numberplate_no_entry.config(state="normal")
        self.car_model_entry.config(state="normal")
        self.engine_entry.config(state="normal")
        self.chassis_no_entry.config(state="normal")
        self.ph_no_entry.config(state="normal")

        self.edit_data_btn.place_forget()
        self.editing_done_data_btn.place(x=65, y=170)



    def edit_vehicle_done_data(self):
        # enable all required fields
        self.editing_done_data_btn.place_forget()
        self.edit_data_btn.place(x=65, y=170)
        self.name_entry.config(state="readonly")
        self.numberplate_no_entry.config(state="readonly")
        self.car_model_entry.config(state="readonly")
        self.engine_entry.config(state="readonly")
        self.chassis_no_entry.config(state="readonly")
        self.ph_no_entry.config(state="readonly")

        self.data[0]["name"] = self.name_var.get()
        self.data[0]["vehicle_no"] = self.numberplate_no_var.get()
        self.data[0]["vehicle_model"] = self.car_model_var.get()
        self.data[0]["engine_no"] = self.engine_var.get()
        self.data[0]["chassis_no"] = self.chassis_no_var.get()
        self.data[0]["ph_no"] = self.ph_no_var.get()
        self.data[0]["vehicle_type"] = self.vehicle_type.get()

        res = database.edit_data_db(self.data)
        if res:
            pass
        else:
            self.name_var.set(self.back_temp['name'])
            self.numberplate_no_var.set(self.back_temp['vehicle_no'])
            self.car_model_var.set(self.back_temp['vehicle_model'])
            self.engine_var.set(self.back_temp['engine_no'])
            self.chassis_no_var.set(self.back_temp['chassis_no'])
            self.ph_no_var.set(self.back_temp['ph_no'])
            self.vehicle_type.set(self.back_temp['vehicle_type'])

            self.data[0]["name"] = self.name_var.get()
            self.data[0]["vehicle_no"] = self.numberplate_no_var.get()
            self.data[0]["vehicle_model"] = self.car_model_var.get()
            self.data[0]["engine_no"] = self.engine_var.get()
            self.data[0]["chassis_no"] = self.chassis_no_var.get()
            self.data[0]["ph_no"] = self.ph_no_var.get()
            self.data[0]["vehicle_type"] = self.vehicle_type.get()
            messagebox.showerror(title="Error", message="Please Check Your internet",
                                 parent=self.main_root)
    def payment_entry_win(self):
        print("payment_entry_win")
        if not self.payment_top_level_open and self.windows == "closed":
            self.payment_top_level_open = True
            self.windows = "open"
            self.payment_top_level = Toplevel(self.main_root)
            self.payment_top_level.title("Car Cue Payment")
            self.payment_top_level.attributes("-topmost", True)
            self.image1111 = Image.open(r"images\raw.png")
            self.photo1111 = ImageTk.PhotoImage(image=self.image1111)
            self.img_lbl1111 = Label(self.payment_top_level, image=self.photo1111)
            self.img_lbl1111.place(x=-2, y=0)


            self.payment_top_level.protocol("WM_DELETE_WINDOW", self.on_close_top_level)
            self.payment_top_level.geometry("1099x600")
            self.payment_top_level.resizable(False, False)
            categories = ["Bank", "UPI", "Cash"]
            self.payment_category = StringVar()

            self.combo_box = ttk.Combobox(self.payment_top_level, state="readonly",
                                          font=("helvatica",self.font_size), textvariable=self.payment_category,
                                          values=categories)
            self.combo_box.place(x=420, y=8)
            self.combo_box.bind("<<ComboboxSelected>>", self.on_combo_select)


            # Create frames for Bank, UPI, and Cash
            self.bank_frame = Frame(self.payment_top_level, height=600, width=1100)
            self.upi_frame = Frame(self.payment_top_level, height=600, width=1100)
            self.cash_frame = Frame(self.payment_top_level, height=600, width=1100)
            self.image11 = Image.open(r"images\bank_entry_bg.png")
            self.photo11 = ImageTk.PhotoImage(image=self.image11)
            self.img_lbl11 = Label(self.bank_frame, image=self.photo11)
            self.img_lbl11.place(x=-2, y=-2)

            self.upi_image11 = Image.open(r"images\upi_entry_bg.png")
            self.upi_photo11 = ImageTk.PhotoImage(image=self.upi_image11)
            self.upi_img_lbl11 = Label(self.upi_frame, image=self.upi_photo11)
            self.upi_img_lbl11.place(x=-2, y=-2)


            self.cash_image11 = Image.open(r"images\cash_entry_bg.png")
            self.cash_photo11 = ImageTk.PhotoImage(image=self.cash_image11)
            self.cash_img_lbl11 = Label(self.cash_frame, image=self.cash_photo11)
            self.cash_img_lbl11.place(x=-2, y=-2)
            # Entries for Bank frame
            # name widget
            self.entry1_bank_var = StringVar()
            self.entry1_bank = Entry(self.bank_frame,
                                    textvariable=self.entry1_bank_var,
                                    validate="key",
                                    bg="#d9d9d9",
                                    borderwidth=0,
                                    font = ("helvatica", self.font_size),
                                    width=self.field_width,
                                    validatecommand=(self.main_root.register(self.validate_name), "%P"),)
            self.entry1_bank.place(x=25, y=33)
            self.entry1_bank.bind('<KeyRelease>', lambda event: self.convert_bank_1_uppercase())

            # account NO. widget
            self.entry2_bank = Entry(self.bank_frame,
                                validate="key",
                                bg="#d9d9d9",
                                borderwidth=0,
                                width=self.field_width,
                                font=("helvatica", self.font_size),
                                validatecommand=(self.main_root.register(self.validate_numerical_only), "%P"),)
            self.entry2_bank.place(x=25, y=85)

            # IFSC widget
            self.entry3_bank_var = StringVar()
            self.entry3_bank = Entry(self.bank_frame,
                                bg="#d9d9d9",
                                textvariable=self.entry3_bank_var,
                                borderwidth=0,
                                width=self.field_width,
                                font=("helvatica", self.font_size),
                                validate="key",
                                validatecommand=(self.main_root.register(self.validate_data), "%P"),)

            self.entry3_bank.place(x=25, y=137)
            self.entry3_bank.bind('<KeyRelease>', lambda event: self.convert_ifsc_uppercase())

            # AMOUNT widget
            self.entry4_bank = Entry(self.bank_frame,
                                validate="key",
                                bg="#d9d9d9",
                                borderwidth=0,
                                width=self.field_width,
                                font=("helvatica", self.font_size),
                                validatecommand=(self.main_root.register(self.validate_numerical_only), "%P"),)
            self.entry4_bank.place(x=25, y=189)

            self.entry_detail_bank_var = StringVar()
            self.entry_detail = Entry(self.bank_frame,
                                validate="key",
                                bg="#d9d9d9",
                                textvariable=self.entry_detail_bank_var,
                                borderwidth=0,
                                width=self.field_width,
                                font=("helvatica", self.font_size),
                                validatecommand=(self.main_root.register(self.validate_data), "%P"),)
            self.entry_detail.place(x=362, y=189)
            self.entry_detail.bind('<KeyRelease>', lambda event: self.convert_bank_details_uppercase())


            self.save_entry_img = ImageTk.PhotoImage(Image.open(r"images\save entry.png"))
            self.save_bank_btn = Button(self.bank_frame,
                                        bg="#b39cd0",
                                        activebackground="#b39cd0",
                                        borderwidth=0,
                                        image=self.save_entry_img, command=self.bank_entry_save)
            self.save_bank_btn.place(x=850, y=88)


            # # ======================================================================
            #
            self.add_bank_var = StringVar()
            self.entry_bank = Entry(self.bank_frame,
                                    validate="key",
                                    bg="#d9d9d9",
                                    borderwidth=0,
                                    width=self.field_width,
                                    textvariable=self.add_bank_var,
                                    font=("helvatica", self.font_size),
                                    validatecommand=(self.main_root.register(self.validate_name), "%P"),)
            self.entry_bank.place(x=362, y=85)
            self.entry_bank.bind('<KeyRelease>', lambda event: self.convert_add_bank_uppercase())

            self.save_bank_img = ImageTk.PhotoImage(Image.open(r"images\SAVE BANK.png"))
            button_save = Button(self.bank_frame,
                                 bg="#b39cd0",
                                 activebackground="#b39cd0",
                                 borderwidth=0,
                                 image=self.save_bank_img, text="Save Bank Name", command=self.save_bank_name)
            button_save.place(x=660, y=78)
            self.bank_name = StringVar()
            self.combobox_bank = ttk.Combobox(self.bank_frame,
                                              state="readonly",
                                              font=("helvatica", self.font_size),
                                              height=4,
                                              textvariable=self.bank_name,)
            self.combobox_bank.place(x=350, y=132)
            self.refresh_combobox()

            self.delete_bank_img = ImageTk.PhotoImage(Image.open(r"images\DELETE BANK.png"))
            button_delete = Button(self.bank_frame,image=self.delete_bank_img,
                                   bg="#b39cd0",
                                   activebackground="#b39cd0",
                                   borderwidth=0,
                                   text="Delete Bank", command=self.delete_bank)
            button_delete.place(x=660, y=132)

            # ======================================================================
            # Entries for UPI frame
            # upi name
            self.entry1_upi_var = StringVar()
            self.entry1_upi = Entry(self.upi_frame,
                               bg="#d9d9d9",
                               borderwidth=0,
                               width=self.field_width,
                               font=("helvatica", self.font_size),
                               textvariable=self.entry1_upi_var,
                               validate="key",
                               validatecommand=(self.main_root.register(self.validate_name), "%P"),)
            self.entry1_upi.place(x=430, y=34)
            self.entry1_upi.bind('<KeyRelease>', lambda event: self.convert_upi_name_uppercase())


            # upi id
            self.entry2_upi_id_var = StringVar()
            self.entry2_upi = Entry(self.upi_frame,
                                bg = "#d9d9d9",
                                borderwidth = 0,
                                width = self.field_width,
                                font = ("helvatica", self.font_size),
                                textvariable=self.entry2_upi_id_var,

                                )
            self.entry2_upi.place(x=430, y=85)
            self.entry2_upi.bind('<KeyRelease>', lambda event: self.convert_upi_id_uppercase())

            #
            # self.result_label = Label(self.upi_frame, text="", wraplength=300, justify='left')
            # self.result_label.place(x=250, y=0)

            self.entry3_upi = Entry(self.upi_frame,
                                    bg="#d9d9d9",
                                    borderwidth=0,
                                    width=self.field_width,
                                    font=("helvatica", self.font_size),
                                    validate="key",
                                    validatecommand=(self.main_root.register(self.validate_numerical_only), "%P"),)
            self.entry3_upi.place(x=430, y=137)

            self.entry_detail_upi_id_var = StringVar()
            self.entry_detail_upi = Entry(self.upi_frame,
                                    bg="#d9d9d9",
                                    borderwidth=0,
                                    textvariable=self.entry_detail_upi_id_var,
                                    width=self.field_width,
                                    font=("helvatica", self.font_size),
                                    validate="key",
                                    validatecommand=(self.main_root.register(self.validate_data), "%P"),)
            self.entry_detail_upi.place(x=430, y=189)
            self.entry_detail_upi.bind('<KeyRelease>', lambda event: self.convert_upi_entry_detail_uppercase())

            # self.entry3_upi.bind("<KeyRelease>", self.convert_to_words)
            #
            self.save_upi_btn = Button(self.upi_frame,
                                       bg="#b39cd0",
                                       activebackground="#b39cd0",
                                       borderwidth=0,
                                       image=self.save_entry_img,
                                       text="SAVE",command=self.upi_entry_save)
            self.save_upi_btn.place(x=801, y=99)

            # Entries for Cash frame
            # cash name
            self.entry1_cash_var = StringVar()
            self.entry1_cash = Entry(self.cash_frame,
                                bg="#d9d9d9",
                                borderwidth=0,
                                font=("helvatica", self.font_size),
                                width=self.field_width,
                                validate="key",
                                textvariable=self.entry1_cash_var,
                                validatecommand=(self.main_root.register(self.validate_name), "%P"),)
            self.entry1_cash.place(x=430, y=44)
            self.entry1_cash.bind('<KeyRelease>', lambda event: self.convert_cash_uppercase())


            self.entry2_cash = Entry(self.cash_frame,
                                bg="#d9d9d9",
                                borderwidth=0,
                                font=("helvatica", self.font_size),
                                width=self.field_width,
                                validate="key",
                                validatecommand=(self.main_root.register(self.validate_numerical_only), "%P"),)
            self.entry2_cash.place(x=430, y=96)

            self.entry_detail_cash_var = StringVar()
            self.entry_detail_cash = Entry(self.cash_frame,
                                bg="#d9d9d9",
                                borderwidth=0,
                                textvariable=self.entry_detail_cash_var,
                                font=("helvatica", self.font_size),
                                width=self.field_width,
                                validate="key",
                                validatecommand=(self.main_root.register(self.validate_data), "%P"),)
            self.entry_detail_cash.place(x=430, y=150)
            self.entry_detail_cash.bind('<KeyRelease>', lambda event: self.convert_entry_detail_cash_uppercase())


            self.save_cash_btn = Button(self.cash_frame,image=self.save_entry_img,
                                        bg="#b39cd0",
                                        activebackground="#b39cd0",
                                        borderwidth=0,
                                        command=self.cash_entry_save)
            self.save_cash_btn.place(x=801, y=99)

            # Initially hide all frames
            self.bank_frame.place_forget()
            self.upi_frame.place_forget()
            self.cash_frame.place_forget()
            self.bank_entries_treeview()
            self.upi_entries_treeview()
            self.cash_entries_treeview()

    def on_close_top_level(self):
        self.payment_top_level_open = False
        self.windows = "closed"
        self.payment_top_level.destroy()

    def on_combo_select(self, event):
        selected_category = self.combo_box.get()
        if selected_category == "Bank":
            self.bank_frame.place(x=0, y=50)
            self.upi_frame.place_forget()
            self.cash_frame.place_forget()
        elif selected_category == "UPI":
            self.bank_frame.place_forget()
            self.upi_frame.place(x=0, y=50)
            self.cash_frame.place_forget()
        elif selected_category == "Cash":
            self.bank_frame.place_forget()
            self.upi_frame.place_forget()
            self.cash_frame.place(x=0, y=50)

    def validate_numerical_only(self, numerical):
        # Define the regular expression pattern for a 10-digit phone number

        # return re.match(r'^[0-9]+$', numerical) is not None
        pattern = r'^[0-9]+$'
        if re.match(pattern, numerical) or numerical == "":
            print(f'Accepted: {numerical}')
            return True
        else:
            print(f'Rejected: {numerical}')
            return False
    def bank_entry_save(self):
        if check_internet.check_internet() == True:
            self.backup_data = copy.deepcopy(self.data)
            self.backup_work_data = copy.deepcopy(self.work_data)
            bank_data = \
                [
                    self.entry1_bank.get(),
                    self.entry2_bank.get(),
                    self.entry3_bank.get(),
                    self.entry4_bank.get(),
                    self.bank_name.get(),
                    self.current_date_fun(),
                    self.current_time_fun(),
                    self.entry_detail.get(),

                ]


            if bank_data[0] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter NAME".upper(),)
            elif bank_data[1] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter ACCOUNT NUMBER".upper(),)
            elif bank_data[2] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter IFSC  number".upper())
            elif bank_data[3] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter amount".upper())
            elif bank_data[4] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please select bank name".upper())
            else:
                from functions import unique_id_fun
                unique_id = unique_id_fun()
                data = {"bank_transactions":
                            {unique_id:
                                 {'a_no': bank_data[1],
                                  'amount': bank_data[3],
                                  'bank': bank_data[4],
                                  'date': bank_data[5],
                                  'ifsc': bank_data[2],
                                  'name': bank_data[0],
                                  'node_name': unique_id,
                                  'time': bank_data[6],
                                  'entry_detail': bank_data[7]
                                  }
                             }
                        }
                if "bank_transactions" not in self.work_data:
                    self.work_data["bank_transactions"] = {}
                self.work_data["bank_transactions"].update(data["bank_transactions"])
                self.update_data(self.all_data, self.data[0])


                # setup total recieved amount in offline data and also updating it in gui
                self.data[0]["recieved_amount"] = self.data[0]["recieved_amount"] + int(bank_data[3])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])

                # setup total due amount in offline data and also updating it in gui
                self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                self.due_amount_var.set(self.data[0]["due_amount"])


                # res = database.save_bank_entry(self.work_data, self.data)
                res = database.run_with_timeout(database.save_bank_entry, args=(self.work_data, self.data),
                                                timeout=10)
                if res == True:
                    messagebox.showinfo(parent=self.payment_top_level, title="Done", message="Entry saved successfully")
                    self.payment_top_level_open = False
                    self.windows = "closed"
                    self.payment_top_level.destroy()
                else:
                    messagebox.showerror(title="Error", message="Please Check Your internet",
                                         parent=self.payment_top_level)
                    self.data[0].update(self.backup_data[0])
                    self.work_data = self.backup_work_data
                    self.total_amount_var.set(self.data[0]["total_amount"])
                    self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                    self.due_amount_var.set(self.data[0]["due_amount"])
            # self.main_root.destroy()
            # obj = commercial_cars_home_win.Main()
            # obj.Home()
        else:
            messagebox.showwarning("connection error", "Please check your internet connection!",
                                   parent=self.payment_top_level)
    def upi_entry_save(self):
        if check_internet.check_internet() == True:
            self.backup_data = copy.deepcopy(self.data)
            self.backup_work_data = copy.deepcopy(self.work_data)
            upi_data = \
                [
                    self.entry1_upi.get(),
                    self.entry2_upi.get(),
                    self.entry3_upi.get(),
                    self.current_date_fun(),
                    self.current_time_fun(),
                    self.entry_detail_upi.get(),

                ]
            if upi_data[0] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter NAME".upper(),)
            elif upi_data[1] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter upi id".upper(),)
            elif upi_data[2] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter amount".upper())

            else:
                from functions import unique_id_fun
                unique_id = unique_id_fun()
                data = {"upi_transactions":
                            {unique_id:
                                {
                                    "name": upi_data[0],
                                    "upi": upi_data[1],
                                    "amount": upi_data[2],
                                    "date": upi_data[3],
                                    "time": upi_data[4],
                                    "entry_detail": upi_data[5],
                                    "node_name": unique_id,
                                 }
                            }
                        }

                if "upi_transactions" not in self.work_data:
                    self.work_data["upi_transactions"] = {}
                self.work_data["upi_transactions"].update(data["upi_transactions"])
                self.update_data(self.all_data, self.data[0])


                # setup total recieved amount in offline data and also updating it in gui
                self.data[0]["recieved_amount"] = self.data[0]["recieved_amount"] + int(upi_data[2])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])

                # setup total due amount in offline data and also updating it in gui
                self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                self.due_amount_var.set(self.data[0]["due_amount"])

                # database.save_upi_entry(self.work_data, self.data)
                res = database.run_with_timeout(database.save_upi_entry, args=(self.work_data, self.data),
                                                timeout=1)
                if res == True:
                    messagebox.showinfo(parent=self.payment_top_level,title="Done",message="Entry saved successfully")
                    self.payment_top_level_open = False
                    self.windows = "closed"
                    self.payment_top_level.destroy()
                else:
                    messagebox.showerror(title="Error", message="Please Check Your internet",
                                         parent=self.payment_top_level)
                    self.data[0].update(self.backup_data[0])
                    self.work_data = self.backup_work_data
                    self.total_amount_var.set(self.data[0]["total_amount"])
                    self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                    self.due_amount_var.set(self.data[0]["due_amount"])
        else:
            messagebox.showwarning("connection error", "Please check your internet connection!",
                                   parent=self.payment_top_level)
    def cash_entry_save(self):
        if check_internet.check_internet() == True:
            self.backup_data = copy.deepcopy(self.data)
            self.backup_work_data = copy.deepcopy(self.work_data)
            cash_data = \
                [
                    self.entry1_cash.get(),
                    self.entry2_cash.get(),
                    self.current_date_fun(),
                    self.current_time_fun(),
                    self.entry_detail_cash.get(),
                ]
            if cash_data[0] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter NAME".upper(),)
            elif cash_data[1] == "":
                messagebox.showwarning(parent=self.payment_top_level,title="Fill all details",message="Please enter amount".upper(),)
            else:
                from functions import unique_id_fun
                unique_id = unique_id_fun()
                data = { "cash_transactions":
                            {unique_id:
                                 {"name": cash_data[0],
                                    "amount": cash_data[1],
                                    "date": cash_data[2],
                                    "time": cash_data[3],
                                    'node_name': unique_id,
                                    'entry_detail': cash_data[4],
                                 }
                            }
                        }
                if "cash_transactions" not in self.work_data:
                    self.work_data["cash_transactions"] = {}
                self.work_data["cash_transactions"].update(data["cash_transactions"])
                self.update_data(self.all_data, self.data[0])


                # setup total recieved amount in offline data and also updating it in gui
                self.data[0]["recieved_amount"] = self.data[0]["recieved_amount"] + int(cash_data[1])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])

                # setup total due amount in offline data and also updating it in gui
                self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                self.due_amount_var.set(self.data[0]["due_amount"])


                # database.save_cash_entry(data, self.data)
                res = database.run_with_timeout(database.save_cash_entry, args=(self.work_data, self.data),
                                                timeout=10)
                if res == True:
                    messagebox.showinfo(parent=self.payment_top_level,title="Done",message="Entry saved successfully")
                    self.payment_top_level_open = False
                    self.windows = "closed"
                    self.payment_top_level.destroy()
                else:
                    messagebox.showerror(title="Error", message="Please Check Your internet",
                                         parent=self.payment_top_level)
                    self.data[0].update(self.backup_data[0])
                    self.work_data = self.backup_work_data
                    self.total_amount_var.set(self.data[0]["total_amount"])
                    self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                    self.due_amount_var.set(self.data[0]["due_amount"])
        else:
            messagebox.showwarning("connection error", "Please check your internet connection!",
                                   parent=self.payment_top_level)
    def refresh_combobox(self):
        if os.path.exists("bank_names.txt"):
            with open("bank_names.txt", "r") as file:
                bank_names = [line.strip() for line in file.readlines()]
            self.combobox_bank['values'] = bank_names
    def save_bank_name(self):
        if self.entry_bank.get() != "":
            bank_name = self.entry_bank.get()
            with open("bank_names.txt", "a") as file:
                file.write(bank_name + "\n")
            self.entry_bank.delete(0, END)
            self.refresh_combobox()
    def delete_bank(self):
        selected_bank = self.combobox_bank.get()
        if selected_bank:
            with open("bank_names.txt", "r") as file:
                bank_names = [line.strip() for line in file.readlines()]
            if selected_bank in bank_names:
                bank_names.remove(selected_bank)
                with open("bank_names.txt", "w") as file:
                    for bank in bank_names:
                        file.write(bank + "\n")
            self.refresh_combobox()
            self.combobox_bank.set("")  # Clear the Combobox selection
    def convert_bank_1_uppercase(self):
        current_text = self.entry1_bank_var.get()
        uppercase_text = current_text.upper()
        self.entry1_bank_var.set(uppercase_text)
    def convert_ifsc_uppercase(self):
        current_text = self.entry3_bank_var.get()
        uppercase_text = current_text.upper()
        self.entry3_bank_var.set(uppercase_text)

    def convert_bank_details_uppercase(self):
        current_text = self.entry_detail.get()
        uppercase_text = current_text.upper()
        self.entry_detail_bank_var.set(uppercase_text)
    def convert_add_bank_uppercase(self):
        print("ho ho")
        current_text = self.add_bank_var.get()
        uppercase_text = current_text.upper()
        self.add_bank_var.set(uppercase_text)
    def convert_upi_name_uppercase(self):
        print("ho ho")
        current_text = self.entry1_upi_var.get()
        uppercase_text = current_text.upper()
        self.entry1_upi_var.set(uppercase_text)
    def convert_upi_id_uppercase(self):
        print("ho ho")
        current_text = self.entry2_upi_id_var.get()
        uppercase_text = current_text.upper()
        self.entry2_upi_id_var.set(uppercase_text)

    def convert_upi_entry_detail_uppercase(self):
        print("ho ho")
        current_text = self.entry_detail_upi.get()
        uppercase_text = current_text.upper()
        self.entry_detail_upi_id_var.set(uppercase_text)
    def convert_cash_uppercase(self):
        print("ho ho")
        current_text = self.entry1_cash_var.get()
        uppercase_text = current_text.upper()
        self.entry1_cash_var.set(uppercase_text)

    def convert_entry_detail_cash_uppercase(self):
        print("ho ho")
        current_text = self.entry_detail_cash.get()
        uppercase_text = current_text.upper()
        self.entry_detail_cash_var.set(uppercase_text)
    def bank_entries_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", stretch=False, font=(None, 10, "bold"),)
        style.configure("Treeview", rowheight=35)
        self.bank_tv = ttk.Treeview(self.bank_frame, columns=("1", "2", "3", "4", "5", "6", "7", "8", "9"),
                               show='headings',
                               height=8)

        self.bank_tv.column("#1", anchor=CENTER, stretch=NO, width=200, minwidth=200)
        self.bank_tv.column("#2", anchor=CENTER, stretch=NO, width=200, minwidth=200)
        self.bank_tv.column("#3", anchor=CENTER, stretch=NO, width=130, minwidth=130)
        self.bank_tv.column("#4", anchor=CENTER, stretch=NO, width=110, minwidth=110)
        self.bank_tv.column("#5", anchor=CENTER, stretch=NO, width=158, minwidth=158)
        self.bank_tv.column("#6", anchor=CENTER, stretch=NO, width=105, minwidth=105)
        self.bank_tv.column("#7", anchor=CENTER, stretch=NO, width=90, minwidth=90)
        self.bank_tv.column("#8", anchor=CENTER, stretch=NO, width=90, minwidth=90)
        self.bank_tv.column("#9", anchor=CENTER, stretch=NO, width=0, minwidth=0)


        self.bank_tv.heading("#1", text='Name')
        self.bank_tv.heading("#2", text='AC.No')
        self.bank_tv.heading("#3", text='IFSC')
        self.bank_tv.heading("#4", text='BANK')
        self.bank_tv.heading("#5", text='PURPOSE')
        self.bank_tv.heading("#6", text='AMOUNT')
        self.bank_tv.heading("#7", text='Time')
        self.bank_tv.heading("#8", text='Date')
        self.bank_tv.heading("#9", text='Id')
        # self.commercial_car_data = db_credentials.get_bank_entries(self.data[0]["Id"])
        # self.res = self.commercial_car_data
        try:
        # if True:
            self.work_data = database.get_work_data(self.data[0]["Id"])
            print(f'bank_treeview----{self.work_data["bank_transactions"]}')
            data = self.work_data["bank_transactions"]
            all_bank_entries = list(data.keys())
            # print(all_bank_entries)
            commercial_car_data = []
            for i in range(0,len(all_bank_entries)):
                # print(i)
                commercial_car_data.append(data[all_bank_entries[i]])

            print(f"commercial_car_data ----- {commercial_car_data}")
            commercial_car_data = sorted(commercial_car_data, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", '%d-%m-%Y %I:%M:%S %p'))

        # print(self.commercial_car_data[0]["name"])
            if len(commercial_car_data) > 0:
                for i in range(0, len(commercial_car_data)):
                    self.bank_tv.insert("", "end", values=(
                        commercial_car_data[i]["name"],
                        commercial_car_data[i]["a_no"],
                        commercial_car_data[i]["ifsc"],
                        commercial_car_data[i]["bank"],
                        commercial_car_data[i]["entry_detail"],
                        commercial_car_data[i]["amount"],
                        commercial_car_data[i]["time"],
                        commercial_car_data[i]["date"],
                        commercial_car_data[i]["node_name"],
                        )
                    )
                    # ================================================================

                self.bank_tv.bind('<Double-Button-1>', self.bank_action)
                self.bank_tv.place(x=6, y=230)
                return self.bank_tv
            else:
                pass
                # messagebox.showinfo("ERROR", "BANK TREEVIEW")
            # self.No_data()
        except KeyError:
            pass
        except:
            messagebox.showerror("","KeyError: 'bank_transactions'")

    def bank_action(self, e):
        # if check_internet.check_internet() == True:
        if True:

            if True:

                # print("i am e",e)
                # get the values of the selected rows\\
                tt = self.bank_tv.focus()
                col = self.bank_tv.identify_column(e.x)
                # row = self.tv.identify_row(e.y)
                # print(f"""
                #             tt ____________ {tt}
                #             col ____________ {col}
                #             row ____________ {row}
                #             """)

                # row = int(row) - 1
                # print(f"row ____________ {row}")

                self.row_data = self.bank_tv.item(tt, "values")
                # self.line_id = self.id_["values"]

                # self.res = self.commercial_car_data
                if col == '#1':
                    response = messagebox.askyesno(parent=self.payment_top_level, title="Confirmation", message="Do you really want to delete this transaction")
                    if response:
                        transaction_id = self.row_data[8]
                        transaction_amount = self.row_data[5]
                        car_id = self.data[0]["Id"]
                        total_recieved = self.data[0]["recieved_amount"] - int(transaction_amount)
                        total_due = self.data[0]["due_amount"] + int(transaction_amount)

                        data = {
                            "transaction_id" : transaction_id,
                            "transaction_amount" : transaction_amount,
                            "car_id" : car_id,
                            "total_recieved" : total_recieved,
                            "total_due" : total_due,
                        }


                        database.delete_bank_entry(data)
                        # print(self.work_data["bank_transactions"][self.row_data[8]])
                        print(f"transaction_id : {transaction_id}")
                        print(f"transaction_amount : {transaction_amount}")
                        print(f"car_id : {car_id}")
                        print(f"total_recieved : {total_recieved}")
                        print(f"total_due : {total_due}")


                        for record in self.data:
                            if record['Id'] == car_id:
                                record['recieved_amount'] = total_recieved
                                record['due_amount'] = total_due
                                break
                        self.update_data(self.all_data, self.data[0])
                        self.update_all_work_amount_entries()
                        self.payment_top_level_open = False
                        self.windows = "closed"
                        self.payment_top_level.destroy()
                else:
                    pass
                    # messagebox.showinfo("Alert", "Something went wrong")
        # else:
        #     messagebox.showwarning("connection error", "Please check your internet connection!",
        #                            parent=self.payment_top_level)


    def upi_entries_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", stretch=False, font=(None, 10, "bold"),)
        style.configure("Treeview", rowheight=35)
        self.upi_tv = ttk.Treeview(self.upi_frame, columns=("1", "2", "3", "4", "5", "6","7"),
                               show='headings',
                               height=8)

        self.upi_tv.column("#1", anchor=CENTER, stretch=NO, width=240, minwidth=240)
        self.upi_tv.column("#2", anchor=CENTER, stretch=NO, width=243, minwidth=243)
        self.upi_tv.column("#3", anchor=CENTER, stretch=NO, width=300, minwidth=300)
        self.upi_tv.column("#4", anchor=CENTER, stretch=NO, width=100, minwidth=100)
        self.upi_tv.column("#5", anchor=CENTER, stretch=NO, width=100, minwidth=100)
        self.upi_tv.column("#6", anchor=CENTER, stretch=NO, width=100, minwidth=100)
        self.upi_tv.column("#7", anchor=CENTER, stretch=NO, width=0, minwidth=0)



        self.upi_tv.heading("#1", text='NAME')
        self.upi_tv.heading("#2", text='UPI ID')
        self.upi_tv.heading("#3", text='PURPOSE')
        self.upi_tv.heading("#4", text='AMOUNT')
        self.upi_tv.heading("#5", text='TIME')
        self.upi_tv.heading("#6", text='DATE')
        self.upi_tv.heading("#7", text='ID')


        try:
            # if True:
            print(f'upi_treeview----{self.work_data["upi_transactions"]}')
            # data = self.data[0]["upi_transactions"]
            data = self.work_data["upi_transactions"]
            all_upi_entries = list(data.keys())
            # print(all_bank_entries)
            commercial_car_data = []
            for i in range(0, len(all_upi_entries)):
                # print(i)
                commercial_car_data.append(data[all_upi_entries[i]])
            commercial_car_data = sorted(commercial_car_data, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", '%d-%m-%Y %I:%M:%S %p'))
        # print(self.commercial_car_data[0]["name"])
            if len(commercial_car_data) > 0:
                for i in range(0, len(commercial_car_data)):
                    self.upi_tv.insert("", "end", values=(
                        commercial_car_data[i]["name"],
                        commercial_car_data[i]["upi"],
                        commercial_car_data[i]["entry_detail"],
                        commercial_car_data[i]["amount"],
                        commercial_car_data[i]["time"],
                        commercial_car_data[i]["date"],
                        commercial_car_data[i]["node_name"],

                        )
                    )
                    # ================================================================
                # self.upi_tv.bind('<Double-Button-1>', self.actions)
                self.upi_tv.bind('<Double-Button-1>', self.upi_action)
                self.upi_tv.place(x=6, y=230)
                return self.upi_tv
            else:
                pass
                # messagebox.showinfo("ERROR", "BANK TREEVIEW")
            # self.No_data()
        except KeyError:
            pass
        except:
            messagebox.showerror("","KeyError: 'upi_transactions'")
            # messagebox.showerror("","KeyError: 'upi_transactions'")


        # self.upi_entries_all = db_credentials.get_upi_entries(self.data[0]["Id"])
        # self.upi_entries_all = self.upi_entries_all
        # print(self.commercial_car_data[0]["name"])
        # if self.upi_entries_all != False:
        #     for i in range(0, len(self.upi_entries_all)):
        #         print(i)
        #         self.tv.insert("", "end", iid=self.upi_entries_all[i]["id"], values=(
        #             self.upi_entries_all[i]["name"],
        #             self.upi_entries_all[i]["upi"],
        #             self.upi_entries_all[i]["amount"],
        #             self.upi_entries_all[i]["time"],
        #             self.upi_entries_all[i]["date"],
        #             self.upi_entries_all[i]["id"],
        #         )
        #                        )
        #         # ================================================================
        #     # self.tv.bind('<Double-Button-1>', self.actions)hj
        #
        #     self.tv.place(x=6, y=230)
        #     return self.tv
        # else:
        #     pass
        #     # messagebox.showinfo("ERROR", "BANK TREEVIEW")
        #     # self.No_data()

    def upi_action(self, e):
        # try:
        if True:

            # print("i am e",e)
            # get the values of the selected rows\\
            tt = self.upi_tv.focus()
            col = self.upi_tv.identify_column(e.x)
            # row = self.tv.identify_row(e.y)
            # print(f"""
            #             tt ____________ {tt}
            #             col ____________ {col}
            #             row ____________ {row}
            #             """)

            # row = int(row) - 1
            # print(f"row ____________ {row}")

            self.row_data = self.upi_tv.item(tt, "values")
            # self.line_id = self.id_["values"]

            # self.res = self.commercial_car_data
            if col == '#1':
                response = messagebox.askyesno(parent=self.payment_top_level, title="Confirmation", message="Do you really want to delete this transaction")
                if response:
                    transaction_id = self.row_data[6]
                    transaction_amount = self.row_data[3]
                    car_id = self.data[0]["Id"]
                    total_recieved = self.data[0]["recieved_amount"] - int(transaction_amount)
                    total_due = self.data[0]["due_amount"] + int(transaction_amount)

                    data = {
                        "transaction_id" : transaction_id,
                        "transaction_amount" : transaction_amount,
                        "car_id" : car_id,
                        "total_recieved" : total_recieved,
                        "total_due" : total_due,
                    }


                    database.delete_upi_entry(data)
                    # print(self.work_data["bank_transactions"][self.row_data[8]])
                    print(f"transaction_id : {transaction_id}")
                    print(f"transaction_amount : {transaction_amount}")
                    print(f"car_id : {car_id}")
                    print(f"total_recieved : {total_recieved}")
                    print(f"total_due : {total_due}")


                    for record in self.data:
                        if record['Id'] == car_id:
                            record['recieved_amount'] = total_recieved
                            record['due_amount'] = total_due
                            break
                    self.update_data(self.all_data, self.data[0])
                    self.update_all_work_amount_entries()
                    self.payment_top_level_open = False
                    self.windows = "closed"
                    self.payment_top_level.destroy()
            else:
                pass
                # messagebox.showinfo("Alert", "Something went wrong")

    def cash_entries_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", stretch=False, font=(None, 10, "bold"),)
        style.configure("Treeview", rowheight=35)
        self.cash_tv = ttk.Treeview(self.cash_frame, columns=("1", "2", "3", "4", "5", "6"),
                               show='headings',
                               height=8)

        self.cash_tv.column("#1", anchor=CENTER, stretch=NO, width=283, minwidth=283)
        self.cash_tv.column("#2", anchor=CENTER, stretch=NO, width=400, minwidth=400)
        self.cash_tv.column("#3", anchor=CENTER, stretch=NO, width=130, minwidth=130)
        self.cash_tv.column("#4", anchor=CENTER, stretch=NO, width=135, minwidth=135)
        self.cash_tv.column("#5", anchor=CENTER, stretch=NO, width=135, minwidth=135)
        self.cash_tv.column("#6", anchor=CENTER, stretch=NO, width=0, minwidth=0)



        self.cash_tv.heading("#1", text='NAME')
        self.cash_tv.heading("#2", text='PURPOSE')
        self.cash_tv.heading("#3", text='AMOUNT')
        self.cash_tv.heading("#4", text='TIME')
        self.cash_tv.heading("#5", text='DATE')
        self.cash_tv.heading("#6", text='ID')

        try:
            # if True:
            print(f'cash_treeview----{self.work_data["cash_transactions"]}')
            # data = self.data[0]["cash_transactions"]
            data = self.work_data["cash_transactions"]
            all_cash_entries = list(data.keys())
            # print(all_bank_entries)
            commercial_car_data = []
            for i in range(0, len(all_cash_entries)):
                # print(i)
                commercial_car_data.append(data[all_cash_entries[i]])
            commercial_car_data = sorted(commercial_car_data, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", '%d-%m-%Y %I:%M:%S %p'))
        # print(self.commercial_car_data[0]["name"])
            if len(commercial_car_data) > 0:
                for i in range(0, len(commercial_car_data)):
                    print(i)
                    self.cash_tv.insert("", "end", values=(
                        commercial_car_data[i]["name"],
                        commercial_car_data[i]["entry_detail"],
                        commercial_car_data[i]["amount"],
                        commercial_car_data[i]["time"],
                        commercial_car_data[i]["date"],
                        commercial_car_data[i]["node_name"],

                        )
                    )
                    # ================================================================
                # self.cash_tv.bind('<Double-Button-1>', self.actions)

                self.cash_tv.bind('<Double-Button-1>', self.cash_action)
                self.cash_tv.place(x=6, y=230)
                return self.cash_tv
            else:
                pass
                # messagebox.showinfo("ERROR", "BANK TREEVIEW")
            # self.No_data()
        except KeyError:
            pass
        except:
            messagebox.showerror("","KeyError: cash_transactions'")

        # self.cash_entries_all = db_credentials.get_cash_entries(self.data[0]["Id"])
        # self.cash_entries_all = self.cash_entries_all
        # print(f"cash_entries_all  {self.cash_entries_all}")
        # if self.cash_entries_all != False:
        #     for i in range(0, len(self.cash_entries_all)):
        #         print(i)
        #         self.tv.insert("", "end", iid=self.cash_entries_all[i]["id"], values=(
        #             self.cash_entries_all[i]["name"],
        #             self.cash_entries_all[i]["amount"],
        #             self.cash_entries_all[i]["time"],
        #             self.cash_entries_all[i]["date"],
        #             self.cash_entries_all[i]["id"],
        #         )
        #                        )
        #         # ================================================================
        #     # self.tv.bind('<Double-Button-1>', self.actions)
        #
        #     self.tv.place(x=6, y=230)
        #     return self.tv
        # else:
        #     pass
        #     # messagebox.showinfo("ERROR", "BANK TREEVIEW")
        #     # self.No_data()

    def cash_action(self, e):
        # try:
        if True:

            # print("i am e",e)
            # get the values of the selected rows\\
            tt = self.cash_tv.focus()
            col = self.cash_tv.identify_column(e.x)
            # row = self.tv.identify_row(e.y)
            # print(f"""
            #             tt ____________ {tt}
            #             col ____________ {col}
            #             row ____________ {row}
            #             """)

            # row = int(row) - 1
            # print(f"row ____________ {row}")

            self.row_data = self.cash_tv.item(tt, "values")
            # self.line_id = self.id_["values"]

            # self.res = self.commercial_car_data
            if col == '#1':
                response = messagebox.askyesno(parent=self.payment_top_level, title="Confirmation", message="Do you really want to delete this transaction")
                if response:
                    transaction_id = self.row_data[5]
                    transaction_amount = self.row_data[2]
                    car_id = self.data[0]["Id"]
                    total_recieved = self.data[0]["recieved_amount"] - int(transaction_amount)
                    total_due = self.data[0]["due_amount"] + int(transaction_amount)

                    data = {
                        "transaction_id" : transaction_id,
                        "transaction_amount" : transaction_amount,
                        "car_id" : car_id,
                        "total_recieved" : total_recieved,
                        "total_due" : total_due,
                    }


                    database.delete_cash_entry(data)
                    # print(self.work_data["bank_transactions"][self.row_data[8]])
                    print(f"transaction_id : {transaction_id}")
                    print(f"transaction_amount : {transaction_amount}")
                    print(f"car_id : {car_id}")
                    print(f"total_recieved : {total_recieved}")
                    print(f"total_due : {total_due}")


                    for record in self.data:
                        if record['Id'] == car_id:
                            record['recieved_amount'] = total_recieved
                            record['due_amount'] = total_due
                            break
                    self.update_data(self.all_data, self.data[0])
                    self.update_all_work_amount_entries()
                    self.payment_top_level_open = False
                    self.windows = "closed"
                    self.payment_top_level.destroy()
            else:
                pass
                # messagebox.showinfo("Alert", "Something went wrong")

    def update_all_work_amount_entries(self):
        self.total_amount_var.set(str(self.data[0]["total_amount"]))
        self.recieved_amount_var.set(str(self.data[0]["recieved_amount"]))
        self.due_amount_var.set(str(self.data[0]["due_amount"]))    











    def open_redispatch_win(self):
        if not self.redispatch_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.redispatch_top_level_open = True
            self.redispatch_top_level = Toplevel()
            self.redispatch_top_level.protocol("WM_DELETE_WINDOW", self.on_close_redispatch_top_level)
            self.redispatch_top_level.configure(bg='#B39CD0')
            screen_width = self.redispatch_top_level.winfo_screenwidth()
            screen_height = self.redispatch_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.redispatch_top_level.title("RC REDISPATCH")
            self.redispatch_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.redispatch_top_level.winfo_screenwidth()
            screen_height = self.redispatch_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.redispatch_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.redispatch_top_level.resizable(False, False)
            self.redispatch_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\redispatch_bg.png"))
            Label(master=self.redispatch_top_level,
                  image=self.redispatch_bg_img).pack()

            self.redispatch_time_lbl = Label(self.redispatch_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.redispatch_time_lbl.place(x=75,y=51)

            self.redispatch_date_lbl = Label(self.redispatch_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.redispatch_date_lbl.place(x=195, y=51)

            self.redispatch_combo_box = ttk.Combobox(self.redispatch_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.redispatch_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.redispatch_scale = ttk.Scale(self.redispatch_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.redispatch_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.redispatch_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["rc_redispatch_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.redispatch_combo_box['values'] = self.combo_values

            self.redispatch_combo_box.bind('<<ComboboxSelected>>', self.redispatch_combo_fun)
            self.redispatch_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.redispatch_amount_var = StringVar()
            self.redispatch_amount_entry = Entry(self.redispatch_top_level,
                                                 textvariable=self.redispatch_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.redispatch_amount_entry.place(x=60, y=125)

            self.redispatch_app_no_var = StringVar()
            self.redispatch_app_no_entry = Entry(self.redispatch_top_level,
                                         textvariable=self.redispatch_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.redispatch_app_no_entry.place(x=60, y=196)
            self.redispatch_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_redispatch_app_no_to_uppercase())


            self.redispatch_status_var = StringVar()
            self.redispatch_status_var.set("0")
            self.redispatch_status_btn = Button(master=self.redispatch_top_level,
                                                textvariable=self.redispatch_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.redispatch_status_change,
                                                borderwidth=0
                                                )
            self.redispatch_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.redispatch_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_redispatch_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.redispatch_top_level,image=self.delete_but_img,
                   command=self.redispatch_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.redispatch_top_level.mainloop()

    def on_close_redispatch_top_level(self):
        self.redispatch_top_level_open = False
        self.redispatch_top_level.destroy()
        self.windows = "closed"

    def redispatch_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def redispatch_status_change(self):
        if self.redispatch_status_var.get() == "0":
            self.redispatch_status_btn.config(image=self.completed_status_img)
            self.redispatch_status_var.set("1")
            print(self.redispatch_status_var.get())
        elif self.redispatch_status_var.get() == "1":
            self.redispatch_status_btn.config(image=self.pending_status_img)
            self.redispatch_status_var.set("0")
            print(self.redispatch_status_var.get())

    def com_redispatch_entry_fun(self):
        if check_internet.check_internet():
            self.backup_data = copy.deepcopy(self.data)
            self.backup_work_data = copy.deepcopy(self.work_data)
            # print(type(self.redispatch_priority_var.get()))
            if self.redispatch_amount_var.get() == "":
                messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.redispatch_top_level)
            else:
                current_date = datetime.now()
                formatted_date = current_date.strftime("%d-%m-%Y")
                # Set the locale to English (United States)
                current_time = datetime.now().time()
                formatted_time = current_time.strftime("%I:%M:%S %p")
                print(type(self.data))
                self.data1 = self.work_data
                print(self.data)
                print(self.data1)

                # result_data[0]["name"]
                if self.data1.get("rc_redispatch_amount") == None:
                    print("1")
                    print(self.data1)
                    if self.redispatch_entry_selection_var == "NEW ENTRY":
                        print("1.1")
                        self.data1["rc_redispatch_amount"] = self.redispatch_amount_var.get()+","
                        self.data1["rc_redispatch_status"] = self.redispatch_status_var.get()+","
                        self.data1["rc_redispatch_app_no"] = self.redispatch_app_no_var.get()+","
                        self.data1["rc_redispatch_time"] = formatted_time + ","
                        self.data1["rc_redispatch_date"] = formatted_date + ","
                        self.data1["rc_redispatch_priority"] = self.con_value(round(self.redispatch_scale.get()))+","

                        # adding redispatch amount + total amount in local data
                        self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.redispatch_amount_var.get())

                        # updating total amount in gui
                        self.total_amount_var.set(self.data[0]["total_amount"])

                        # calculating due amount = total_amount - recieved_amount
                        self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                        # updating due amount in gui
                        self.due_amount_var.set(self.data[0]["due_amount"])

                        res = database.run_with_timeout(database.com_redispatch_entry, args=(self.data, self.data1),
                                                        timeout=10)

                        if res == True:
                            self.redispatch_top_level.destroy()
                            self.on_close_redispatch_top_level()
                            self.update_data(self.all_data,self.data[0])


                        elif res == False:
                            messagebox.showerror(title="Error", message="Please Check Your internet",
                                                   parent=self.redispatch_top_level)
                            self.data[0].update(self.backup_data[0])
                            self.work_data = self.backup_work_data

                            self.total_amount_var.set(self.data[0]["total_amount"])
                            self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                            self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.data1.get("rc_redispatch_amount") != None:
                    print("2.0")
                    if self.redispatch_entry_selection_var == "NEW ENTRY":
                        print("2.1")
                        self.data1["rc_redispatch_amount"] = self.work_data["rc_redispatch_amount"] +self.redispatch_amount_var.get()+","
                        self.data1["rc_redispatch_status"] = self.work_data["rc_redispatch_status"] +self.redispatch_status_var.get()+","
                        self.data1["rc_redispatch_app_no"] = self.work_data["rc_redispatch_app_no"] +self.redispatch_app_no_var.get()+","

                        self.data1["rc_redispatch_time"] = self.work_data["rc_redispatch_time"] + formatted_time + ","
                        self.data1["rc_redispatch_date"] = self.work_data["rc_redispatch_date"] +formatted_date + ","
                        self.data1["rc_redispatch_priority"] = self.work_data["rc_redispatch_priority"] +self.con_value(round(self.redispatch_scale.get()))+","



                        # adding redispatch amount + total amount in local data
                        self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.redispatch_amount_var.get())

                        # updating total amount in gui
                        self.total_amount_var.set(self.data[0]["total_amount"])

                        # calculating due amount = total_amount - recieved_amount
                        self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                        # updating due amount in gui
                        self.due_amount_var.set(self.data[0]["due_amount"])



                        # res = database.com_redispatch_entry(self.data, self.data1)
                        res = database.run_with_timeout(database.com_redispatch_entry, args=(self.data, self.data1),
                                                        timeout=10)
                        if res == True:
                            self.redispatch_top_level.destroy()
                            self.on_close_redispatch_top_level()
                            self.update_data(self.all_data,self.data[0])

                        elif res == False:
                            messagebox.showerror(title="Error", message="Please Check Your internet",
                                                   parent=self.redispatch_top_level)
                            print(f"---------=========\n{self.data}")
                            print(f"=========---------\n{self.backup_data}")

                            self.data[0].update(self.backup_data[0])
                            self.work_data = self.backup_work_data
                            self.total_amount_var.set(self.data[0]["total_amount"])
                            self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                            self.due_amount_var.set(self.data[0]["due_amount"])

                    elif self.redispatch_entry_selection_var == "MODIFY ENTRY":
                        print("2.2")
                        data = self.work_data["rc_redispatch_amount"].split(',')
                        # removing old amount of redispatch
                        self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                        # adding new amount of redispatch
                        self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.redispatch_amount_var.get())
                        # setting up in total amount
                        self.total_amount_var.set(self.data[0]["total_amount"])



                        # setup total due amount in offline data and also updating it in gui
                        self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                        self.due_amount_var.set(self.data[0]["due_amount"])

                        data = self.work_data["rc_redispatch_amount"].split(',')
                        data[self.index] = self.redispatch_amount_entry.get()
                        data =",".join(data)
                        self.work_data["rc_redispatch_amount"] = data

                        data = self.work_data["rc_redispatch_status"].split(',')
                        data[self.index] = self.redispatch_status_var.get()
                        data =",".join(data)
                        self.work_data["rc_redispatch_status"] = data

                        data = self.work_data["rc_redispatch_app_no"].split(',')
                        data[self.index] = self.redispatch_app_no_var.get()
                        data =",".join(data)
                        self.work_data["rc_redispatch_app_no"] = data


                        data = self.work_data["rc_redispatch_priority"].split(',')
                        data[self.index] = self.con_value(round(self.redispatch_scale.get()))
                        data =",".join(data)
                        self.work_data["rc_redispatch_priority"] = data
                        # messagebox.showinfo(parent=self.redispatch_top_level,title="",message=data)
                        # res = database.com_redispatch_entry(self.data, self.work_data)
                        res = database.run_with_timeout(database.com_redispatch_entry, args=(self.data, self.work_data),
                                                        timeout=10)
                        if res == True:
                            self.redispatch_top_level.destroy()
                            self.on_close_redispatch_top_level()
                            self.update_data(self.all_data,self.data[0])

                        elif res == False:
                            messagebox.showerror(title="Error", message="Please Check Your internet",
                                                   parent=self.redispatch_top_level)

                            self.data[0].update(self.backup_data[0])
                            self.work_data = self.backup_work_data

                            self.total_amount_var.set(self.data[0]["total_amount"])
                            self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                            self.due_amount_var.set(self.data[0]["due_amount"])
        else:
            messagebox.showerror("connection error", "Please check your internet connection!", parent=self.redispatch_top_level)
    def redispatch_combo_fun(self, event):
        if self.redispatch_combo_box.get() == "NEW ENTRY":
            self.redispatch_amount_var.set("")
            self.redispatch_app_no_var.set("")
            self.redispatch_status_var.set("1")
            self.redispatch_status_change()
            self.redispatch_entry_selection_var = "NEW ENTRY"
            self.redispatch_date_lbl.config(text="")
            self.redispatch_time_lbl.config(text="")
            self.redispatch_scale.set(0)


        # self.data[0]["rc_redispatch_amount"]
        else:
            self.redispatch_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.redispatch_combo_box.get())-1
            amount = self.work_data["rc_redispatch_amount"].split(",")
            app_no = self.work_data["rc_redispatch_app_no"].split(",")
            status = self.work_data["rc_redispatch_status"].split(",")
            date = self.work_data["rc_redispatch_date"].split(",")
            time = self.work_data["rc_redispatch_time"].split(",")
            priority = self.work_data["rc_redispatch_priority"].split(",")
            self.redispatch_amount_var.set(amount[int(self.redispatch_combo_box.get())-1])
            self.redispatch_app_no_var.set(app_no[int(self.redispatch_combo_box.get())-1])
            self.redispatch_status_var.set(status[int(self.redispatch_combo_box.get())-1])
            self.redispatch_date_lbl.config(text=date[int(self.redispatch_combo_box.get())-1])
            self.redispatch_time_lbl.config(text=time[int(self.redispatch_combo_box.get())-1])
            self.redispatch_scale.set(self.con_value_rev(priority[int(self.redispatch_combo_box.get())-1]))

            if self.redispatch_status_var.get() == "0":
                self.redispatch_status_btn.config(image=self.pending_status_img)
            elif self.redispatch_status_var.get() == "1":
                self.redispatch_status_btn.config(image=self.completed_status_img)

    def redispatch_entry_delete_fun(self):
        if check_internet.check_internet():
            if self.redispatch_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
                self.backup_data = copy.deepcopy(self.data)
                self.backup_work_data = copy.deepcopy(self.work_data)

                # these three line of code, subtract delete work amount from total
                data = self.work_data["rc_redispatch_amount"].split(',')
                self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                self.total_amount_var.set(self.data[0]["total_amount"])

                # setup total due amount in offline data and also updating it in gui
                self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                self.due_amount_var.set(self.data[0]["due_amount"])

                data = self.work_data["rc_redispatch_amount"].split(',')
                data.pop(self.index)
                data = ",".join(data)
                self.work_data["rc_redispatch_amount"] = data

                data = self.work_data["rc_redispatch_status"].split(',')
                data.pop(self.index)
                data = ",".join(data)
                self.work_data["rc_redispatch_status"] = data

                data = self.work_data["rc_redispatch_app_no"].split(',')
                data.pop(self.index)
                data = ",".join(data)
                self.work_data["rc_redispatch_app_no"] = data

                data = self.work_data["rc_redispatch_date"].split(',')
                data.pop(self.index)
                data = ",".join(data)
                self.work_data["rc_redispatch_date"] = data

                data = self.work_data["rc_redispatch_time"].split(',')
                data.pop(self.index)
                data = ",".join(data)
                self.work_data["rc_redispatch_time"] = data

                data = self.work_data["rc_redispatch_priority"].split(',')
                data.pop(self.index)
                data = ",".join(data)
                self.work_data["rc_redispatch_priority"] = data

                # res = database.com_redispatch_entry(self.data, self.work_data)
                res = database.run_with_timeout(database.com_redispatch_entry, args=(self.data, self.work_data),
                                                timeout=10)
                if res == True:
                    self.redispatch_top_level.destroy()
                    self.on_close_redispatch_top_level()
                    self.update_data(self.all_data, self.data[0])

                elif res == False:
                    messagebox.showerror(title="Error", message="Please Check Your internet",
                                         parent=self.redispatch_top_level)
                    self.data[0].update(self.backup_data[0])
                    self.work_data = self.backup_work_data

                    self.total_amount_var.set(self.data[0]["total_amount"])
                    self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                    self.due_amount_var.set(self.data[0]["due_amount"])
        else:
            messagebox.showerror("connection error", "Please check your internet connection!", parent=self.redispatch_top_level)
    def redispatch_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.redispatch_update_scale_color(value)  # Update scale color based on value

    def convert_redispatch_app_no_to_uppercase(self):
        current_text = self.redispatch_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.redispatch_app_no_var.set(uppercase_text)



















    def open_rc_duplicate_win(self):
        if not self.rc_duplicate_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.rc_duplicate_top_level_open = True
            self.rc_duplicate_top_level = Toplevel()
            self.rc_duplicate_top_level.protocol("WM_DELETE_WINDOW", self.on_close_rc_duplicate_top_level)
            self.rc_duplicate_top_level.configure(bg='#B39CD0')
            screen_width = self.rc_duplicate_top_level.winfo_screenwidth()
            screen_height = self.rc_duplicate_top_level.winfo_screenheight()
            self.rc_duplicate_top_level.title("RC DUPLICATE")
            self.rc_duplicate_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.rc_duplicate_top_level.winfo_screenwidth()
            screen_height = self.rc_duplicate_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.rc_duplicate_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.rc_duplicate_top_level.resizable(False, False)
            self.rc_duplicate_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_duplicate_bg.png"))
            Label(master=self.rc_duplicate_top_level,
                  image=self.rc_duplicate_bg_img).pack()

            self.rc_duplicate_time_lbl = Label(self.rc_duplicate_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.rc_duplicate_time_lbl.place(x=75, y=51)

            self.rc_duplicate_date_lbl = Label(self.rc_duplicate_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.rc_duplicate_date_lbl.place(x=195, y=51)

            self.rc_duplicate_combo_box = ttk.Combobox(self.rc_duplicate_top_level,
                                                     font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.rc_duplicate_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc",
                                 sliderthickness=10,
                                 sliderlength=50)
            # Create a Scale widget using ttk
            self.rc_duplicate_scale = ttk.Scale(self.rc_duplicate_top_level, from_=0, to=2, orient=HORIZONTAL,
                                              command=self.rc_duplicate_on_scale_change,
                                              style="Custom.Horizontal.TScale")
            self.rc_duplicate_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

            self.combo_values = ["NEW ENTRY", ]
            try:
                # this condition checks how many entries are already there in database
                data = self.work_data["rc_duplicate_amount"]
                split_data = data.split(',')
                self.combo_values += [i + 1 for i in range(len(split_data) - 1)]
            except:
                pass
            self.rc_duplicate_combo_box['values'] = self.combo_values

            self.rc_duplicate_combo_box.bind('<<ComboboxSelected>>', self.rc_duplicate_combo_fun)
            self.rc_duplicate_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.rc_duplicate_amount_var = StringVar()
            self.rc_duplicate_amount_entry = Entry(self.rc_duplicate_top_level,
                                                 textvariable=self.rc_duplicate_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.rc_duplicate_amount_entry.place(x=60, y=125)


            self.rc_duplicate_app_no_var = StringVar()
            self.rc_duplicate_app_no_entry = Entry(self.rc_duplicate_top_level,
                                         textvariable=self.rc_duplicate_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.rc_duplicate_app_no_entry.place(x=60, y=196)
            self.rc_duplicate_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_rc_duplicate_app_no_to_uppercase())

            self.rc_duplicate_status_var = StringVar()
            self.rc_duplicate_status_var.set("0")
            self.rc_duplicate_status_btn = Button(master=self.rc_duplicate_top_level,
                                                textvariable=self.rc_duplicate_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.rc_duplicate_status_change,
                                                borderwidth=0
                                                )
            self.rc_duplicate_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.rc_duplicate_top_level, text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_rc_duplicate_entry_fun).place(x=150, y=420)

            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.rc_duplicate_top_level, image=self.delete_but_img,
                   command=self.rc_duplicate_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)

            self.rc_duplicate_top_level.mainloop()
    def on_close_rc_duplicate_top_level(self):
        self.windows = "closed"
        self.rc_duplicate_top_level_open = False
        self.rc_duplicate_top_level.destroy()

    def rc_duplicate_on_scale_change(self, value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.rc_duplicate_update_scale_color(value)  # Update scale color based on value

    def rc_duplicate_update_scale_color(self, value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def rc_duplicate_status_change(self):
        if self.rc_duplicate_status_var.get() == "0":
            self.rc_duplicate_status_btn.config(image=self.completed_status_img)
            self.rc_duplicate_status_var.set("1")
            print(self.rc_duplicate_status_var.get())
        elif self.rc_duplicate_status_var.get() == "1":
            self.rc_duplicate_status_btn.config(image=self.pending_status_img)
            self.rc_duplicate_status_var.set("0")
            print(self.rc_duplicate_status_var.get())

    def com_rc_duplicate_entry_fun(self):
        self.rc_duplicate_backup_data = copy.deepcopy(self.data)
        # print(type(self.redispatch_priority_var.get()))
        if self.rc_duplicate_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field", message="Please Enter Amount", parent=self.rc_duplicate_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("rc_duplicate_amount") == None:
                print("1")
                if self.rc_duplicate_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["rc_duplicate_amount"] = self.rc_duplicate_amount_var.get() + ","
                    self.data1["rc_duplicate_status"] = self.rc_duplicate_status_var.get() + ","
                    self.data1["rc_duplicate_app_no"] = self.rc_duplicate_app_no_var.get() + ","
                    self.data1["rc_duplicate_time"] = formatted_time + ","
                    self.data1["rc_duplicate_date"] = formatted_date + ","
                    self.data1["rc_duplicate_priority"] = self.con_value(round(self.rc_duplicate_scale.get())) + ","



                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_duplicate_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_rc_duplicate_entry(self.data, self.data1)
                    if res == True:
                        self.rc_duplicate_top_level.destroy()
                        self.on_close_rc_duplicate_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                             parent=self.rc_duplicate_top_level)
                        self.data[0].update(self.rc_duplicate_backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

            elif self.data1.get("rc_duplicate_amount") != None:
                print("2.0")
                if self.rc_duplicate_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["rc_duplicate_amount"] = self.work_data[
                                                               "rc_duplicate_amount"] + self.rc_duplicate_amount_var.get() + ","
                    self.data1["rc_duplicate_status"] = self.work_data[
                                                               "rc_duplicate_status"] + self.rc_duplicate_status_var.get() + ","
                    self.data1["rc_duplicate_app_no"] = self.work_data[
                                                               "rc_duplicate_app_no"] + self.rc_duplicate_app_no_var.get() + ","

                    self.data1["rc_duplicate_time"] = self.work_data["rc_duplicate_time"] + formatted_time + ","
                    self.data1["rc_duplicate_date"] = self.work_data["rc_duplicate_date"] + formatted_date + ","
                    self.data1["rc_duplicate_priority"] = self.work_data["rc_duplicate_priority"] + self.con_value(
                        round(self.rc_duplicate_scale.get())) + ","




                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_duplicate_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_rc_duplicate_entry(self.data, self.data1)
                    if res == True:
                        self.rc_duplicate_top_level.destroy()
                        self.on_close_rc_duplicate_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                             parent=self.rc_duplicate_top_level)
                        self.data[0].update(self.rc_duplicate_backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.rc_duplicate_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")
                    data = self.work_data["rc_duplicate_amount"].split(',')

                    # removing old amount of rc duplicate
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of rc duplicate
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_duplicate_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    data = self.work_data["rc_duplicate_amount"].split(',')
                    data[self.index] = self.rc_duplicate_amount_entry.get()
                    data = ",".join(data)
                    self.work_data["rc_duplicate_amount"] = data

                    data = self.work_data["rc_duplicate_status"].split(',')
                    data[self.index] = self.rc_duplicate_status_var.get()
                    data = ",".join(data)
                    self.work_data["rc_duplicate_status"] = data

                    data = self.work_data["rc_duplicate_app_no"].split(',')
                    data[self.index] = self.rc_duplicate_app_no_var.get()
                    data = ",".join(data)
                    self.work_data["rc_duplicate_app_no"] = data

                    data = self.work_data["rc_duplicate_priority"].split(',')
                    data[self.index] = self.con_value(round(self.rc_duplicate_scale.get()))
                    data = ",".join(data)
                    self.work_data["rc_duplicate_priority"] = data
                    # messagebox.showinfo(parent=self.redispatch_top_level,title="",message=data)
                    res = database.com_rc_duplicate_entry(self.data, self.work_data)
                    if res == True:
                        self.rc_duplicate_top_level.destroy()
                        self.on_close_rc_duplicate_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                             parent=self.rc_duplicate_top_level)
                        self.data[0].update(self.rc_duplicate_backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_duplicate_combo_fun(self, event):
        if self.rc_duplicate_combo_box.get() == "NEW ENTRY":
            self.rc_duplicate_amount_var.set("")
            self.rc_duplicate_app_no_var.set("")
            self.rc_duplicate_status_var.set("1")
            self.rc_duplicate_status_change()
            self.rc_duplicate_entry_selection_var = "NEW ENTRY"
            self.rc_duplicate_date_lbl.config(text="")
            self.rc_duplicate_time_lbl.config(text="")
            self.rc_duplicate_scale.set(0)


        # self.data[0]["rc_redispatch_amount"]
        else:
            self.rc_duplicate_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.rc_duplicate_combo_box.get()) - 1
            amount = self.work_data["rc_duplicate_amount"].split(",")
            app_no = self.work_data["rc_duplicate_app_no"].split(",")
            status = self.work_data["rc_duplicate_status"].split(",")
            date = self.work_data["rc_duplicate_date"].split(",")
            time = self.work_data["rc_duplicate_time"].split(",")
            priority = self.work_data["rc_duplicate_priority"].split(",")
            self.rc_duplicate_amount_var.set(amount[int(self.rc_duplicate_combo_box.get()) - 1])
            self.rc_duplicate_app_no_var.set(app_no[int(self.rc_duplicate_combo_box.get()) - 1])
            self.rc_duplicate_status_var.set(status[int(self.rc_duplicate_combo_box.get()) - 1])
            self.rc_duplicate_date_lbl.config(text=date[int(self.rc_duplicate_combo_box.get()) - 1])
            self.rc_duplicate_time_lbl.config(text=time[int(self.rc_duplicate_combo_box.get()) - 1])
            self.rc_duplicate_scale.set(self.con_value_rev(priority[int(self.rc_duplicate_combo_box.get()) - 1]))
            if self.rc_duplicate_status_var.get() == "0":
                self.rc_duplicate_status_btn.config(image=self.pending_status_img)
            elif self.rc_duplicate_status_var.get() == "1":
                self.rc_duplicate_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.redispatch_top_level, title="",message="")

    def rc_duplicate_entry_delete_fun(self):
        if self.rc_duplicate_combo_box.get().isdigit():  # condition checks that if entry available then only deletion works
            self.rc_duplicate_backup_data = copy.deepcopy(self.data)

            # these three line of code, subtract delete work amount from total
            data = self.work_data["rc_duplicate_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])



            data = self.work_data["rc_duplicate_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_duplicate_amount"] = data

            data = self.work_data["rc_duplicate_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_duplicate_app_no"] = data

            data = self.work_data["rc_duplicate_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_duplicate_status"] = data

            data = self.work_data["rc_duplicate_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_duplicate_date"] = data

            data = self.work_data["rc_duplicate_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_duplicate_time"] = data

            data = self.work_data["rc_duplicate_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_duplicate_priority"] = data

            res = database.com_rc_duplicate_entry(self.data, self.work_data)
            if res == True:
                self.rc_duplicate_top_level.destroy()
                self.on_close_rc_duplicate_top_level()
            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.rc_duplicate_top_level)
                self.data = self.rc_duplicate_backup_data

    def convert_rc_duplicate_app_no_to_uppercase(self):
        current_text = self.rc_duplicate_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.rc_duplicate_app_no_var.set(uppercase_text)

















    def open_rc_modify_win(self):   
        if not self.rc_modify_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.rc_modify_top_level_open = True
            self.rc_modify_top_level = Toplevel()
            self.rc_modify_top_level.protocol("WM_DELETE_WINDOW", self.on_close_rc_modify_top_level)
            self.rc_modify_top_level.configure(bg='#B39CD0')
            screen_width = self.rc_modify_top_level.winfo_screenwidth()
            screen_height = self.rc_modify_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.rc_modify_top_level.title("RC MODIFY")
            self.rc_modify_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.rc_modify_top_level.winfo_screenwidth()
            screen_height = self.rc_modify_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.rc_modify_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.rc_modify_top_level.resizable(False, False)
            self.rc_modify_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_modify_bg.png"))
            Label(master=self.rc_modify_top_level,
                  image=self.rc_modify_bg_img).pack()

            self.rc_modify_time_lbl = Label(self.rc_modify_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.rc_modify_time_lbl.place(x=75,y=51)

            self.rc_modify_date_lbl = Label(self.rc_modify_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.rc_modify_date_lbl.place(x=195, y=51)

            self.rc_modify_combo_box = ttk.Combobox(self.rc_modify_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.rc_modify_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.rc_modify_scale = ttk.Scale(self.rc_modify_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.rc_modify_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.rc_modify_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["rc_modify_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.rc_modify_combo_box['values'] = self.combo_values

            self.rc_modify_combo_box.bind('<<ComboboxSelected>>', self.rc_modify_combo_fun)
            self.rc_modify_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.rc_modify_amount_var = StringVar()
            self.rc_modify_amount_entry = Entry(self.rc_modify_top_level,
                                                 textvariable=self.rc_modify_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.rc_modify_amount_entry.place(x=60, y=125)

            self.rc_modify_app_no_var = StringVar()
            self.rc_modify_app_no_entry = Entry(self.rc_modify_top_level,
                                         textvariable=self.rc_modify_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.rc_modify_app_no_entry.place(x=60, y=196)
            self.rc_modify_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_rc_modify_app_no_to_uppercase())



            self.rc_modify_status_var = StringVar()
            self.rc_modify_status_var.set("0")
            self.rc_modify_status_btn = Button(master=self.rc_modify_top_level,
                                                textvariable=self.rc_modify_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.rc_modify_status_change,
                                                borderwidth=0
                                                )
            self.rc_modify_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.rc_modify_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_rc_modify_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.rc_modify_top_level,image=self.delete_but_img,
                   command=self.rc_modify_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.rc_modify_top_level.mainloop()

    def on_close_rc_modify_top_level(self):
        self.windows = "closed"
        self.rc_modify_top_level_open = False
        self.rc_modify_top_level.destroy()

    def rc_modify_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def rc_modify_status_change(self):
        if self.rc_modify_status_var.get() == "0":
            self.rc_modify_status_btn.config(image=self.completed_status_img)
            self.rc_modify_status_var.set("1")
            print(self.rc_modify_status_var.get())
        elif self.rc_modify_status_var.get() == "1":
            self.rc_modify_status_btn.config(image=self.pending_status_img)
            self.rc_modify_status_var.set("0")
            print(self.rc_modify_status_var.get())

    def com_rc_modify_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.rc_modify_priority_var.get()))
        if self.rc_modify_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.rc_modify_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            self.data1 = self.work_data

            print(type(self.data))
            # result_data[0]["name"]
            if self.data1.get("rc_modify_amount") == None:
                print("1")
                if self.rc_modify_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["rc_modify_amount"] = self.rc_modify_amount_var.get()+","
                    self.data1["rc_modify_app_no"] = self.rc_modify_app_no_var.get()+","
                    self.data1["rc_modify_status"] = self.rc_modify_status_var.get()+","
                    self.data1["rc_modify_time"] = formatted_time + ","
                    self.data1["rc_modify_date"] = formatted_date + ","
                    self.data1["rc_modify_priority"] = self.con_value(round(self.rc_modify_scale.get()))+","



                    # adding rc modify amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_modify_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_rc_modify_entry(self.data, self.data1)
                    if res == True:
                        self.rc_modify_top_level.destroy()
                        self.on_close_rc_modify_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_modify_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("rc_modify_amount") != None:
                print("2.0")
                if self.rc_modify_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["rc_modify_amount"] = self.work_data["rc_modify_amount"] +self.rc_modify_amount_var.get()+","
                    self.data1["rc_modify_app_no"] = self.work_data["rc_modify_app_no"] +self.rc_modify_app_no_var.get()+","
                    self.data1["rc_modify_status"] = self.work_data["rc_modify_status"] +self.rc_modify_status_var.get()+","
                    self.data1["rc_modify_time"] = self.work_data["rc_modify_time"] + formatted_time + ","
                    self.data1["rc_modify_date"] = self.work_data["rc_modify_date"] +formatted_date + ","
                    self.data1["rc_modify_priority"] = self.work_data["rc_modify_priority"] +self.con_value(round(self.rc_modify_scale.get()))+","



                    # adding rc modify amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_modify_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_rc_modify_entry(self.data, self.data1)
                    if res == True:
                        self.rc_modify_top_level.destroy()
                        self.on_close_rc_modify_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_modify_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.rc_modify_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")



                    data = self.work_data["rc_modify_amount"].split(',')
                    # removing old amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_modify_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["rc_modify_amount"].split(',')
                    data[self.index] = self.rc_modify_amount_entry.get()
                    data =",".join(data)
                    self.work_data["rc_modify_amount"] = data

                    data = self.work_data["rc_modify_app_no"].split(',')
                    data[self.index] = self.rc_modify_app_no_var.get()
                    data =",".join(data)
                    self.work_data["rc_modify_app_no"] = data

                    data = self.work_data["rc_modify_status"].split(',')
                    data[self.index] = self.rc_modify_status_var.get()
                    data =",".join(data)
                    self.work_data["rc_modify_status"] = data

                    data = self.work_data["rc_modify_priority"].split(',')
                    data[self.index] = self.con_value(round(self.rc_modify_scale.get()))
                    data =",".join(data)
                    self.work_data["rc_modify_priority"] = data
                    # messagebox.showinfo(parent=self.rc_modify_top_level,title="",message=data)
                    res = database.com_rc_modify_entry(self.data, self.work_data)
                    if res == True:
                        self.rc_modify_top_level.destroy()
                        self.on_close_rc_modify_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_modify_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_modify_combo_fun(self, event):
        if self.rc_modify_combo_box.get() == "NEW ENTRY":
            self.rc_modify_amount_var.set("")
            self.rc_modify_app_no_var.set("")
            self.rc_modify_status_var.set("1")
            self.rc_modify_status_change()
            self.rc_modify_entry_selection_var = "NEW ENTRY"
            self.rc_modify_date_lbl.config(text="")
            self.rc_modify_time_lbl.config(text="")
            self.rc_modify_scale.set(0)


        # self.data[0]["rc_modify_amount"]
        else:
            self.rc_modify_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.rc_modify_combo_box.get())-1
            amount = self.work_data["rc_modify_amount"].split(",")
            app_no = self.work_data["rc_modify_app_no"].split(",")
            status = self.work_data["rc_modify_status"].split(",")
            date = self.work_data["rc_modify_date"].split(",")
            time = self.work_data["rc_modify_time"].split(",")
            priority = self.work_data["rc_modify_priority"].split(",")
            self.rc_modify_amount_var.set(amount[int(self.rc_modify_combo_box.get())-1])
            self.rc_modify_app_no_var.set(app_no[int(self.rc_modify_combo_box.get())-1])
            self.rc_modify_status_var.set(status[int(self.rc_modify_combo_box.get())-1])
            self.rc_modify_date_lbl.config(text=date[int(self.rc_modify_combo_box.get())-1])
            self.rc_modify_time_lbl.config(text=time[int(self.rc_modify_combo_box.get())-1])
            self.rc_modify_scale.set(self.con_value_rev(priority[int(self.rc_modify_combo_box.get())-1]))
            if self.rc_modify_status_var.get() == "0":
                self.rc_modify_status_btn.config(image=self.pending_status_img)
            elif self.rc_modify_status_var.get() == "1":
                self.rc_modify_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.rc_modify_top_level, title="",message="")

    def rc_modify_entry_delete_fun(self):
        if self.rc_modify_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["rc_modify_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["rc_modify_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_modify_amount"] = data

            data = self.work_data["rc_modify_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_modify_app_no"] = data

            data = self.work_data["rc_modify_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_modify_status"] = data

            data = self.work_data["rc_modify_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_modify_date"] = data

            data = self.work_data["rc_modify_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_modify_time"] = data

            data = self.work_data["rc_modify_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_modify_priority"] = data

            res = database.com_rc_modify_entry(self.data, self.work_data)
            if res == True:
                self.rc_modify_top_level.destroy()
                self.on_close_rc_modify_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.rc_modify_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_modify_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.rc_modify_update_scale_color(value)  # Update scale color based on value

    def convert_rc_modify_app_no_to_uppercase(self):
        current_text = self.rc_modify_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.rc_modify_app_no_var.set(uppercase_text)













    def open_rc_transfer_win(self):
        if not self.rc_transfer_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.rc_transfer_top_level_open = True
            self.rc_transfer_top_level = Toplevel()
            self.rc_transfer_top_level.protocol("WM_DELETE_WINDOW", self.on_close_rc_transfer_top_level)
            self.rc_transfer_top_level.configure(bg='#B39CD0')
            screen_width = self.rc_transfer_top_level.winfo_screenwidth()
            screen_height = self.rc_transfer_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.rc_transfer_top_level.title("RC TRANSFER")
            self.rc_transfer_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.rc_transfer_top_level.winfo_screenwidth()
            screen_height = self.rc_transfer_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.rc_transfer_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.rc_transfer_top_level.resizable(False, False)
            self.rc_transfer_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_transfer_bg.png"))
            Label(master=self.rc_transfer_top_level,
                  image=self.rc_transfer_bg_img).pack()

            self.rc_transfer_time_lbl = Label(self.rc_transfer_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.rc_transfer_time_lbl.place(x=75,y=51)

            self.rc_transfer_date_lbl = Label(self.rc_transfer_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.rc_transfer_date_lbl.place(x=195, y=51)

            self.rc_transfer_combo_box = ttk.Combobox(self.rc_transfer_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.rc_transfer_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.rc_transfer_scale = ttk.Scale(self.rc_transfer_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.rc_transfer_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.rc_transfer_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["rc_transfer_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.rc_transfer_combo_box['values'] = self.combo_values

            self.rc_transfer_combo_box.bind('<<ComboboxSelected>>', self.rc_transfer_combo_fun)
            self.rc_transfer_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.rc_transfer_amount_var = StringVar()
            self.rc_transfer_amount_entry = Entry(self.rc_transfer_top_level,
                                                 textvariable=self.rc_transfer_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.rc_transfer_amount_entry.place(x=60, y=125)

            self.rc_transfer_name_var = StringVar()
            self.rc_transfer_name_entry = Entry(master=self.rc_transfer_top_level,
                                                textvariable=self.rc_transfer_name_var,
                                                validate="key",
                                                # state="disabled",
                                                validatecommand=(self.main_root.register(self.validate_name), "%P"),
                                                bg=self.color_1, border=0,
                                                disabledbackground=self.color_1,
                                                width=self.field_width_2,
                                                font=("Helvetica", self.font_size))
            self.rc_transfer_name_entry.place(x=60, y=196)

            self.rc_transfer_app_no_var = StringVar()
            self.rc_transfer_app_no_entry = Entry(self.rc_transfer_top_level,
                                         textvariable=self.rc_transfer_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.rc_transfer_app_no_entry.place(x=300, y=196)
            self.rc_transfer_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_rc_transfer_app_no_to_uppercase())


            self.rc_transfer_status_var = StringVar()
            self.rc_transfer_status_var.set("0")
            self.rc_transfer_status_btn = Button(master=self.rc_transfer_top_level,
                                                textvariable=self.rc_transfer_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.rc_transfer_status_change,
                                                borderwidth=0
                                                )
            self.rc_transfer_status_btn.place(x=250, y=125)

            self.rc_transfer_name_entry.bind('<KeyRelease>', lambda event: self.rc_transfer_to_uppercase())

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.rc_transfer_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_rc_transfer_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.rc_transfer_top_level,image=self.delete_but_img,
                   command=self.rc_transfer_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.rc_transfer_top_level.mainloop()

    def on_close_rc_transfer_top_level(self):
        self.windows = "closed"
        self.rc_transfer_top_level_open = False
        self.rc_transfer_top_level.destroy()

    def rc_transfer_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def rc_transfer_status_change(self):
        if self.rc_transfer_status_var.get() == "0":
            self.rc_transfer_status_btn.config(image=self.completed_status_img)
            self.rc_transfer_status_var.set("1")
            print(self.rc_transfer_status_var.get())
        elif self.rc_transfer_status_var.get() == "1":
            self.rc_transfer_status_btn.config(image=self.pending_status_img)
            self.rc_transfer_status_var.set("0")
            print(self.rc_transfer_status_var.get())

    def com_rc_transfer_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.rc_transfer_priority_var.get()))
        if self.rc_transfer_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.rc_transfer_top_level)
        elif self.rc_transfer_name_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Name",parent=self.rc_transfer_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("rc_transfer_amount") == None:
                print("1")
                if self.rc_transfer_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["rc_transfer_amount"] = self.rc_transfer_amount_var.get()+","
                    self.data1["rc_transfer_app_no"] = self.rc_transfer_app_no_var.get()+","
                    self.data1["rc_transfer_status"] = self.rc_transfer_status_var.get()+","
                    self.data1["rc_transfer_time"] = formatted_time + ","
                    self.data1["rc_transfer_date"] = formatted_date + ","
                    self.data1["rc_transfer_priority"] = self.con_value(round(self.rc_transfer_scale.get()))+","
                    self.data1["rc_transfer_name"] = self.rc_transfer_name_var.get()+","




                    # adding rc transfer amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_transfer_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_rc_transfer_entry(self.data, self.data1)
                    if res == True:
                        self.rc_transfer_top_level.destroy()
                        self.on_close_rc_transfer_top_level()
                        self.update_data(self.all_data,self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_transfer_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("rc_transfer_amount") != None:
                print("2.0")
                if self.rc_transfer_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["rc_transfer_amount"] = self.work_data["rc_transfer_amount"] +self.rc_transfer_amount_var.get()+","
                    self.data1["rc_transfer_app_no"] = self.work_data["rc_transfer_app_no"] +self.rc_transfer_app_no_var.get()+","
                    self.data1["rc_transfer_status"] = self.work_data["rc_transfer_status"] +self.rc_transfer_status_var.get()+","
                    self.data1["rc_transfer_time"] = self.work_data["rc_transfer_time"] + formatted_time + ","
                    self.data1["rc_transfer_date"] = self.work_data["rc_transfer_date"] +formatted_date + ","
                    self.data1["rc_transfer_priority"] = self.work_data["rc_transfer_priority"] +self.con_value(round(self.rc_transfer_scale.get()))+","
                    self.data1["rc_transfer_name"] = self.work_data["rc_transfer_name"] +self.rc_transfer_name_var.get()+","

                    # adding rc transfer amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_transfer_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])


                    res = database.com_rc_transfer_entry(self.data, self.data1)
                    if res == True:
                        self.rc_transfer_top_level.destroy()
                        self.on_close_rc_transfer_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_transfer_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.rc_transfer_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["rc_transfer_amount"].split(',')
                    # removing old amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_transfer_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    data = self.work_data["rc_transfer_amount"].split(',')
                    data[self.index] = self.rc_transfer_amount_entry.get()
                    data =",".join(data)
                    self.work_data["rc_transfer_amount"] = data

                    data = self.work_data["rc_transfer_app_no"].split(',')
                    data[self.index] = self.rc_transfer_app_no_var.get()
                    data =",".join(data)
                    self.work_data["rc_transfer_app_no"] = data

                    data = self.work_data["rc_transfer_status"].split(',')
                    data[self.index] = self.rc_transfer_status_var.get()
                    data =",".join(data)
                    self.work_data["rc_transfer_status"] = data

                    data = self.work_data["rc_transfer_priority"].split(',')
                    data[self.index] = self.con_value(round(self.rc_transfer_scale.get()))
                    data =",".join(data)
                    self.work_data["rc_transfer_priority"] = data

                    data = self.work_data["rc_transfer_name"].split(',')
                    data[self.index] = self.rc_transfer_name_var.get()
                    data = ",".join(data)
                    self.work_data["rc_transfer_name"] = data
                    # messagebox.showinfo(parent=self.rc_transfer_top_level,title="",message=data)
                    res = database.com_rc_transfer_entry(self.data, self.work_data)
                    if res == True:
                        self.rc_transfer_top_level.destroy()
                        self.on_close_rc_transfer_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_transfer_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_transfer_combo_fun(self, event):
        if self.rc_transfer_combo_box.get() == "NEW ENTRY":
            self.rc_transfer_amount_var.set("")
            self.rc_transfer_app_no_var.set("")
            self.rc_transfer_status_var.set("1")
            self.rc_transfer_status_change()
            self.rc_transfer_entry_selection_var = "NEW ENTRY"
            self.rc_transfer_date_lbl.config(text="")
            self.rc_transfer_time_lbl.config(text="")
            self.rc_transfer_scale.set(0)
            self.rc_transfer_name_var.set("")


        # self.data[0]["rc_transfer_amount"]
        else:
            self.rc_transfer_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.rc_transfer_combo_box.get())-1
            amount = self.work_data["rc_transfer_amount"].split(",")
            app_no = self.work_data["rc_transfer_app_no"].split(",")
            status = self.work_data["rc_transfer_status"].split(",")
            date = self.work_data["rc_transfer_date"].split(",")
            time = self.work_data["rc_transfer_time"].split(",")
            priority = self.work_data["rc_transfer_priority"].split(",")
            transfer_name = self.work_data["rc_transfer_name"].split(",")
            self.rc_transfer_amount_var.set(amount[int(self.rc_transfer_combo_box.get())-1])
            self.rc_transfer_app_no_var.set(app_no[int(self.rc_transfer_combo_box.get())-1])
            self.rc_transfer_status_var.set(status[int(self.rc_transfer_combo_box.get())-1])
            self.rc_transfer_date_lbl.config(text=date[int(self.rc_transfer_combo_box.get())-1])
            self.rc_transfer_time_lbl.config(text=time[int(self.rc_transfer_combo_box.get())-1])
            self.rc_transfer_scale.set(self.con_value_rev(priority[int(self.rc_transfer_combo_box.get())-1]))
            self.rc_transfer_name_var.set(transfer_name[int(self.rc_transfer_combo_box.get())-1])
            if self.rc_transfer_status_var.get() == "0":
                self.rc_transfer_status_btn.config(image=self.pending_status_img)
            elif self.rc_transfer_status_var.get() == "1":
                self.rc_transfer_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.rc_transfer_top_level, title="",message="")

    def rc_transfer_entry_delete_fun(self):
        if self.rc_transfer_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["rc_transfer_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["rc_transfer_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_transfer_amount"] = data

            data = self.work_data["rc_transfer_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_transfer_app_no"] = data

            data = self.work_data["rc_transfer_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_transfer_status"] = data

            data = self.work_data["rc_transfer_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_transfer_date"] = data

            data = self.work_data["rc_transfer_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_transfer_time"] = data

            data = self.work_data["rc_transfer_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_transfer_priority"] = data

            data = self.work_data["rc_transfer_name"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_transfer_name"] = data
            res = database.com_rc_transfer_entry(self.data, self.work_data)
            if res == True:
                self.rc_transfer_top_level.destroy()
                self.on_close_rc_transfer_top_level()
                self.update_data(self.all_data, self.data[0])
            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.rc_transfer_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_transfer_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.rc_transfer_update_scale_color(value)  # Update scale color based on value

    def convert_rc_transfer_app_no_to_uppercase(self):

        current_text = self.rc_transfer_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.rc_transfer_app_no_var.set(uppercase_text)
















    def open_rc_conversion_win(self):
        if not self.rc_conversion_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.rc_conversion_top_level_open = True
            self.rc_conversion_top_level = Toplevel()
            self.rc_conversion_top_level.protocol("WM_DELETE_WINDOW", self.on_close_rc_conversion_top_level)
            self.rc_conversion_top_level.configure(bg='#B39CD0')
            screen_width = self.rc_conversion_top_level.winfo_screenwidth()
            screen_height = self.rc_conversion_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.rc_conversion_top_level.title("RC CONVERSION")
            self.rc_conversion_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.rc_conversion_top_level.winfo_screenwidth()
            screen_height = self.rc_conversion_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.rc_conversion_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.rc_conversion_top_level.resizable(False, False)
            self.rc_conversion_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_conversion_bg.png"))
            Label(master=self.rc_conversion_top_level,
                  image=self.rc_conversion_bg_img).pack()

            self.rc_conversion_time_lbl = Label(self.rc_conversion_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.rc_conversion_time_lbl.place(x=75,y=51)

            self.rc_conversion_date_lbl = Label(self.rc_conversion_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.rc_conversion_date_lbl.place(x=195, y=51)

            self.rc_conversion_combo_box = ttk.Combobox(self.rc_conversion_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.rc_conversion_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.rc_conversion_scale = ttk.Scale(self.rc_conversion_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.rc_conversion_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.rc_conversion_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["rc_conversion_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.rc_conversion_combo_box['values'] = self.combo_values

            self.rc_conversion_combo_box.bind('<<ComboboxSelected>>', self.rc_conversion_combo_fun)
            self.rc_conversion_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.rc_conversion_amount_var = StringVar()
            self.rc_conversion_amount_entry = Entry(self.rc_conversion_top_level,
                                                 textvariable=self.rc_conversion_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.rc_conversion_amount_entry.place(x=60, y=125)

            self.rc_conversion_app_no_var = StringVar()
            self.rc_conversion_app_no_entry = Entry(self.rc_conversion_top_level,
                                         textvariable=self.rc_conversion_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.rc_conversion_app_no_entry.place(x=60, y=196)
            self.rc_conversion_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_rc_conversion_app_no_to_uppercase())


            self.rc_conversion_status_var = StringVar()
            self.rc_conversion_status_var.set("0")
            self.rc_conversion_status_btn = Button(master=self.rc_conversion_top_level,
                                                textvariable=self.rc_conversion_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.rc_conversion_status_change,
                                                borderwidth=0
                                                )
            self.rc_conversion_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.rc_conversion_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_rc_conversion_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.rc_conversion_top_level,image=self.delete_but_img,
                   command=self.rc_conversion_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.rc_conversion_top_level.mainloop()

    def on_close_rc_conversion_top_level(self):
        self.rc_conversion_top_level_open = False
        self.rc_conversion_top_level.destroy()
        self.windows = "closed"

    def rc_conversion_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def rc_conversion_status_change(self):
        if self.rc_conversion_status_var.get() == "0":
            self.rc_conversion_status_btn.config(image=self.completed_status_img)
            self.rc_conversion_status_var.set("1")
            print(self.rc_conversion_status_var.get())
        elif self.rc_conversion_status_var.get() == "1":
            self.rc_conversion_status_btn.config(image=self.pending_status_img)
            self.rc_conversion_status_var.set("0")
            print(self.rc_conversion_status_var.get())

    def com_rc_conversion_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.rc_conversion_priority_var.get()))
        if self.rc_conversion_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.rc_conversion_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("rc_conversion_amount") == None:
                print("1")
                if self.rc_conversion_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["rc_conversion_amount"] = self.rc_conversion_amount_var.get()+","
                    self.data1["rc_conversion_app_no"] = self.rc_conversion_app_no_var.get()+","
                    self.data1["rc_conversion_status"] = self.rc_conversion_status_var.get()+","
                    self.data1["rc_conversion_time"] = formatted_time + ","
                    self.data1["rc_conversion_date"] = formatted_date + ","
                    self.data1["rc_conversion_priority"] = self.con_value(round(self.rc_conversion_scale.get()))+","




                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_conversion_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_rc_conversion_entry(self.data, self.data1)
                    if res == True:
                        self.rc_conversion_top_level.destroy()
                        self.on_close_rc_conversion_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_conversion_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("rc_conversion_amount") != None:
                print("2.0")
                if self.rc_conversion_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["rc_conversion_amount"] = self.work_data["rc_conversion_amount"] +self.rc_conversion_amount_var.get()+","
                    self.data1["rc_conversion_app_no"] = self.work_data["rc_conversion_app_no"] +self.rc_conversion_app_no_var.get()+","
                    self.data1["rc_conversion_status"] = self.work_data["rc_conversion_status"] +self.rc_conversion_status_var.get()+","
                    self.data1["rc_conversion_time"] = self.work_data["rc_conversion_time"] + formatted_time + ","
                    self.data1["rc_conversion_date"] = self.work_data["rc_conversion_date"] +formatted_date + ","
                    self.data1["rc_conversion_priority"] = self.work_data["rc_conversion_priority"] +self.con_value(round(self.rc_conversion_scale.get()))+","





                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_conversion_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_rc_conversion_entry(self.data, self.data1)
                    if res == True:
                        self.rc_conversion_top_level.destroy()
                        self.on_close_rc_conversion_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_conversion_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.rc_conversion_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")





                    data = self.work_data["rc_conversion_amount"].split(',')
                    # removing old amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_conversion_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    data = self.work_data["rc_conversion_amount"].split(',')
                    data[self.index] = self.rc_conversion_amount_entry.get()
                    data =",".join(data)
                    self.work_data["rc_conversion_amount"] = data

                    data = self.work_data["rc_conversion_app_no"].split(',')
                    data[self.index] = self.rc_conversion_app_no_var.get()
                    data =",".join(data)
                    self.work_data["rc_conversion_app_no"] = data

                    data = self.work_data["rc_conversion_status"].split(',')
                    data[self.index] = self.rc_conversion_status_var.get()
                    data =",".join(data)
                    self.work_data["rc_conversion_status"] = data

                    data = self.work_data["rc_conversion_priority"].split(',')
                    data[self.index] = self.con_value(round(self.rc_conversion_scale.get()))
                    data =",".join(data)
                    self.work_data["rc_conversion_priority"] = data
                    # messagebox.showinfo(parent=self.rc_conversion_top_level,title="",message=data)
                    res = database.com_rc_conversion_entry(self.data, self.work_data)
                    if res == True:
                        self.rc_conversion_top_level.destroy()
                        self.on_close_rc_conversion_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_conversion_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_conversion_combo_fun(self, event):
        if self.rc_conversion_combo_box.get() == "NEW ENTRY":
            self.rc_conversion_amount_var.set("")
            self.rc_conversion_app_no_var.set("")
            self.rc_conversion_status_var.set("1")
            self.rc_conversion_status_change()
            self.rc_conversion_entry_selection_var = "NEW ENTRY"
            self.rc_conversion_date_lbl.config(text="")
            self.rc_conversion_time_lbl.config(text="")
            self.rc_conversion_scale.set(0)


        # self.data[0]["rc_conversion_amount"]
        else:
            self.rc_conversion_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.rc_conversion_combo_box.get())-1
            amount = self.work_data["rc_conversion_amount"].split(",")
            app_no = self.work_data["rc_conversion_app_no"].split(",")
            status = self.work_data["rc_conversion_status"].split(",")
            date = self.work_data["rc_conversion_date"].split(",")
            time = self.work_data["rc_conversion_time"].split(",")
            priority = self.work_data["rc_conversion_priority"].split(",")
            self.rc_conversion_amount_var.set(amount[int(self.rc_conversion_combo_box.get())-1])
            self.rc_conversion_app_no_var.set(app_no[int(self.rc_conversion_combo_box.get())-1])
            self.rc_conversion_status_var.set(status[int(self.rc_conversion_combo_box.get())-1])
            self.rc_conversion_date_lbl.config(text=date[int(self.rc_conversion_combo_box.get())-1])
            self.rc_conversion_time_lbl.config(text=time[int(self.rc_conversion_combo_box.get())-1])
            self.rc_conversion_scale.set(self.con_value_rev(priority[int(self.rc_conversion_combo_box.get())-1]))
            if self.rc_conversion_status_var.get() == "0":
                self.rc_conversion_status_btn.config(image=self.pending_status_img)
            elif self.rc_conversion_status_var.get() == "1":
                self.rc_conversion_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.rc_conversion_top_level, title="",message="")

    def rc_conversion_entry_delete_fun(self):
        if self.rc_conversion_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)



            # these three line of code, subtract delete work amount from total
            data = self.work_data["rc_conversion_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["rc_conversion_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_conversion_amount"] = data

            data = self.work_data["rc_conversion_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_conversion_app_no"] = data

            data = self.work_data["rc_conversion_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_conversion_status"] = data

            data = self.work_data["rc_conversion_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_conversion_date"] = data

            data = self.work_data["rc_conversion_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_conversion_time"] = data

            data = self.work_data["rc_conversion_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_conversion_priority"] = data

            res = database.com_rc_conversion_entry(self.data, self.work_data)
            if res == True:
                self.rc_conversion_top_level.destroy()
                self.on_close_rc_conversion_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.rc_conversion_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_conversion_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.rc_conversion_update_scale_color(value)  # Update scale color based on value

    def convert_rc_conversion_app_no_to_uppercase(self):
        current_text = self.rc_conversion_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.rc_conversion_app_no_var.set(uppercase_text)




















    def open_hp_cancel_win(self):
        if not self.hp_cancel_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.hp_cancel_top_level_open = True
            self.hp_cancel_top_level = Toplevel()
            self.hp_cancel_top_level.protocol("WM_DELETE_WINDOW", self.on_close_hp_cancel_top_level)
            self.hp_cancel_top_level.configure(bg='#B39CD0')
            screen_width = self.hp_cancel_top_level.winfo_screenwidth()
            screen_height = self.hp_cancel_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.hp_cancel_top_level.title("HP CANCEL")
            self.hp_cancel_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.hp_cancel_top_level.winfo_screenwidth()
            screen_height = self.hp_cancel_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.hp_cancel_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.hp_cancel_top_level.resizable(False, False)
            self.hp_cancel_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\hp_cancel_bg.png"))
            Label(master=self.hp_cancel_top_level,
                  image=self.hp_cancel_bg_img).pack()

            self.hp_cancel_time_lbl = Label(self.hp_cancel_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.hp_cancel_time_lbl.place(x=75,y=51)

            self.hp_cancel_date_lbl = Label(self.hp_cancel_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.hp_cancel_date_lbl.place(x=195, y=51)

            self.hp_cancel_combo_box = ttk.Combobox(self.hp_cancel_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.hp_cancel_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.hp_cancel_scale = ttk.Scale(self.hp_cancel_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.hp_cancel_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.hp_cancel_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["hp_cancel_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.hp_cancel_combo_box['values'] = self.combo_values

            self.hp_cancel_combo_box.bind('<<ComboboxSelected>>', self.hp_cancel_combo_fun)
            self.hp_cancel_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.hp_cancel_amount_var = StringVar()
            self.hp_cancel_amount_entry = Entry(self.hp_cancel_top_level,
                                                 textvariable=self.hp_cancel_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.hp_cancel_amount_entry.place(x=60, y=125)

            self.hp_cancel_app_no_var = StringVar()
            self.hp_cancel_app_no_entry = Entry(self.hp_cancel_top_level,
                                         textvariable=self.hp_cancel_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.hp_cancel_app_no_entry.place(x=60, y=196)
            self.hp_cancel_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_hp_cancel_app_no_to_uppercase())

            self.hp_cancel_status_var = StringVar()
            self.hp_cancel_status_var.set("0")
            self.hp_cancel_status_btn = Button(master=self.hp_cancel_top_level,
                                                textvariable=self.hp_cancel_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.hp_cancel_status_change,
                                                borderwidth=0
                                                )
            self.hp_cancel_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.hp_cancel_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_hp_cancel_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.hp_cancel_top_level,image=self.delete_but_img,
                   command=self.hp_cancel_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.hp_cancel_top_level.mainloop()

    def on_close_hp_cancel_top_level(self):
        self.hp_cancel_top_level_open = False
        self.hp_cancel_top_level.destroy()
        self.windows = "closed"

    def hp_cancel_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def hp_cancel_status_change(self):
        if self.hp_cancel_status_var.get() == "0":
            self.hp_cancel_status_btn.config(image=self.completed_status_img)
            self.hp_cancel_status_var.set("1")
            print(self.hp_cancel_status_var.get())
        elif self.hp_cancel_status_var.get() == "1":
            self.hp_cancel_status_btn.config(image=self.pending_status_img)
            self.hp_cancel_status_var.set("0")
            print(self.hp_cancel_status_var.get())

    def com_hp_cancel_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.hp_cancel_priority_var.get()))
        if self.hp_cancel_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.hp_cancel_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("hp_cancel_amount") == None:
                print("1")
                if self.hp_cancel_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["hp_cancel_amount"] = self.hp_cancel_amount_var.get()+","
                    self.data1["hp_cancel_app_no"] = self.hp_cancel_app_no_var.get()+","
                    self.data1["hp_cancel_status"] = self.hp_cancel_status_var.get()+","
                    self.data1["hp_cancel_time"] = formatted_time + ","
                    self.data1["hp_cancel_date"] = formatted_date + ","
                    self.data1["hp_cancel_priority"] = self.con_value(round(self.hp_cancel_scale.get()))+","



                    # adding hp cancel amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hp_cancel_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_hp_cancel_entry(self.data, self.data1)
                    if res == True:
                        self.hp_cancel_top_level.destroy()
                        self.on_close_hp_cancel_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hp_cancel_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("hp_cancel_amount") != None:
                print("2.0")
                if self.hp_cancel_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["hp_cancel_amount"] = self.work_data["hp_cancel_amount"] +self.hp_cancel_amount_var.get()+","
                    self.data1["hp_cancel_app_no"] = self.work_data["hp_cancel_app_no"] +self.hp_cancel_app_no_var.get()+","
                    self.data1["hp_cancel_status"] = self.work_data["hp_cancel_status"] +self.hp_cancel_status_var.get()+","
                    self.data1["hp_cancel_time"] = self.work_data["hp_cancel_time"] + formatted_time + ","
                    self.data1["hp_cancel_date"] = self.work_data["hp_cancel_date"] +formatted_date + ","
                    self.data1["hp_cancel_priority"] = self.work_data["hp_cancel_priority"] +self.con_value(round(self.hp_cancel_scale.get()))+","




                    # adding hp cancel amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hp_cancel_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_hp_cancel_entry(self.data, self.data1)
                    if res == True:
                        self.hp_cancel_top_level.destroy()
                        self.on_close_hp_cancel_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hp_cancel_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.hp_cancel_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["hp_cancel_amount"].split(',')
                    # removing old amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hp_cancel_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["hp_cancel_amount"].split(',')
                    data[self.index] = self.hp_cancel_amount_entry.get()
                    data =",".join(data)
                    self.work_data["hp_cancel_amount"] = data

                    data = self.work_data["hp_cancel_app_no"].split(',')
                    data[self.index] = self.hp_cancel_app_no_var.get()
                    data =",".join(data)
                    self.work_data["hp_cancel_app_no"] = data

                    data = self.work_data["hp_cancel_status"].split(',')
                    data[self.index] = self.hp_cancel_status_var.get()
                    data =",".join(data)
                    self.work_data["hp_cancel_status"] = data

                    data = self.work_data["hp_cancel_priority"].split(',')
                    data[self.index] = self.con_value(round(self.hp_cancel_scale.get()))
                    data =",".join(data)
                    self.work_data["hp_cancel_priority"] = data
                    # messagebox.showinfo(parent=self.hp_cancel_top_level,title="",message=data)
                    res = database.com_hp_cancel_entry(self.data, self.work_data)
                    if res == True:
                        self.hp_cancel_top_level.destroy()
                        self.on_close_hp_cancel_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hp_cancel_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def hp_cancel_combo_fun(self, event):
        if self.hp_cancel_combo_box.get() == "NEW ENTRY":
            self.hp_cancel_amount_var.set("")
            self.hp_cancel_app_no_var.set("")
            self.hp_cancel_status_var.set("1")
            self.hp_cancel_status_change()
            self.hp_cancel_entry_selection_var = "NEW ENTRY"
            self.hp_cancel_date_lbl.config(text="")
            self.hp_cancel_time_lbl.config(text="")
            self.hp_cancel_scale.set(0)


        # self.data[0]["hp_cancel_amount"]
        else:
            self.hp_cancel_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.hp_cancel_combo_box.get())-1
            amount = self.work_data["hp_cancel_amount"].split(",")
            app_no = self.work_data["hp_cancel_app_no"].split(",")
            status = self.work_data["hp_cancel_status"].split(",")
            date = self.work_data["hp_cancel_date"].split(",")
            time = self.work_data["hp_cancel_time"].split(",")
            priority = self.work_data["hp_cancel_priority"].split(",")
            self.hp_cancel_amount_var.set(amount[int(self.hp_cancel_combo_box.get())-1])
            self.hp_cancel_app_no_var.set(app_no[int(self.hp_cancel_combo_box.get())-1])
            self.hp_cancel_status_var.set(status[int(self.hp_cancel_combo_box.get())-1])
            self.hp_cancel_date_lbl.config(text=date[int(self.hp_cancel_combo_box.get())-1])
            self.hp_cancel_time_lbl.config(text=time[int(self.hp_cancel_combo_box.get())-1])
            self.hp_cancel_scale.set(self.con_value_rev(priority[int(self.hp_cancel_combo_box.get())-1]))
            if self.hp_cancel_status_var.get() == "0":
                self.hp_cancel_status_btn.config(image=self.pending_status_img)
            elif self.hp_cancel_status_var.get() == "1":
                self.hp_cancel_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.hp_cancel_top_level, title="",message="")

    def hp_cancel_entry_delete_fun(self):
        if self.hp_cancel_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["hp_cancel_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["hp_cancel_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_cancel_amount"] = data

            data = self.work_data["hp_cancel_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_cancel_app_no"] = data

            data = self.work_data["hp_cancel_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_cancel_status"] = data

            data = self.work_data["hp_cancel_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_cancel_date"] = data

            data = self.work_data["hp_cancel_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_cancel_time"] = data

            data = self.work_data["hp_cancel_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_cancel_priority"] = data

            res = database.com_hp_cancel_entry(self.data, self.work_data)
            if res == True:
                self.hp_cancel_top_level.destroy()
                self.on_close_hp_cancel_top_level()
                self.update_data(self.all_data, self.data[0])


            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.hp_cancel_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def hp_cancel_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.hp_cancel_update_scale_color(value)  # Update scale color based on value

    def convert_hp_cancel_app_no_to_uppercase(self):
        current_text = self.hp_cancel_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.hp_cancel_app_no_var.set(uppercase_text)






















    def open_hp_made_win(self):
        if not self.hp_made_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.hp_made_top_level_open = True
            self.hp_made_top_level = Toplevel()
            self.hp_made_top_level.protocol("WM_DELETE_WINDOW", self.on_close_hp_made_top_level)
            self.hp_made_top_level.configure(bg='#B39CD0')
            screen_width = self.hp_made_top_level.winfo_screenwidth()
            screen_height = self.hp_made_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.hp_made_top_level.title("HP MADE")
            self.hp_made_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.hp_made_top_level.winfo_screenwidth()
            screen_height = self.hp_made_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.hp_made_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.hp_made_top_level.resizable(False, False)
            self.hp_made_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\hp_made_bg.png"))
            Label(master=self.hp_made_top_level,
                  image=self.hp_made_bg_img).pack()

            self.hp_made_time_lbl = Label(self.hp_made_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.hp_made_time_lbl.place(x=75,y=51)

            self.hp_made_date_lbl = Label(self.hp_made_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.hp_made_date_lbl.place(x=195, y=51)

            self.hp_made_combo_box = ttk.Combobox(self.hp_made_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.hp_made_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.hp_made_scale = ttk.Scale(self.hp_made_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.hp_made_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.hp_made_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["hp_made_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.hp_made_combo_box['values'] = self.combo_values

            self.hp_made_combo_box.bind('<<ComboboxSelected>>', self.hp_made_combo_fun)
            self.hp_made_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.hp_made_amount_var = StringVar()
            self.hp_made_amount_entry = Entry(self.hp_made_top_level,
                                                 textvariable=self.hp_made_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.hp_made_amount_entry.place(x=60, y=125)

            self.hp_made_app_no_var = StringVar()
            self.hp_made_app_no_entry = Entry(self.hp_made_top_level,
                                         textvariable=self.hp_made_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.hp_made_app_no_entry.place(x=60, y=196)
            self.hp_made_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_hp_made_app_no_to_uppercase())


            self.hp_made_status_var = StringVar()
            self.hp_made_status_var.set("0")
            self.hp_made_status_btn = Button(master=self.hp_made_top_level,
                                                textvariable=self.hp_made_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.hp_made_status_change,
                                                borderwidth=0
                                                )
            self.hp_made_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.hp_made_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_hp_made_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.hp_made_top_level,image=self.delete_but_img,
                   command=self.hp_made_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.hp_made_top_level.mainloop()

    def on_close_hp_made_top_level(self):
        self.hp_made_top_level_open = False
        self.hp_made_top_level.destroy()
        self.windows = "closed"

    def hp_made_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def hp_made_status_change(self):
        if self.hp_made_status_var.get() == "0":
            self.hp_made_status_btn.config(image=self.completed_status_img)
            self.hp_made_status_var.set("1")
            print(self.hp_made_status_var.get())
        elif self.hp_made_status_var.get() == "1":
            self.hp_made_status_btn.config(image=self.pending_status_img)
            self.hp_made_status_var.set("0")
            print(self.hp_made_status_var.get())

    def com_hp_made_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.hp_made_priority_var.get()))
        if self.hp_made_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.hp_made_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("hp_made_amount") == None:
                print("1")
                if self.hp_made_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["hp_made_amount"] = self.hp_made_amount_var.get()+","
                    self.data1["hp_made_app_no"] = self.hp_made_app_no_var.get()+","
                    self.data1["hp_made_status"] = self.hp_made_status_var.get()+","
                    self.data1["hp_made_time"] = formatted_time + ","
                    self.data1["hp_made_date"] = formatted_date + ","
                    self.data1["hp_made_priority"] = self.con_value(round(self.hp_made_scale.get()))+","




                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hp_made_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_hp_made_entry(self.data, self.data1)
                    if res == True:
                        self.hp_made_top_level.destroy()
                        self.on_close_hp_made_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hp_made_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("hp_made_amount") != None:
                print("2.0")
                if self.hp_made_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["hp_made_amount"] = self.work_data["hp_made_amount"] +self.hp_made_amount_var.get()+","
                    self.data1["hp_made_app_no"] = self.work_data["hp_made_app_no"] +self.hp_made_app_no_var.get()+","
                    self.data1["hp_made_status"] = self.work_data["hp_made_status"] +self.hp_made_status_var.get()+","
                    self.data1["hp_made_time"] = self.work_data["hp_made_time"] + formatted_time + ","
                    self.data1["hp_made_date"] = self.work_data["hp_made_date"] +formatted_date + ","
                    self.data1["hp_made_priority"] = self.work_data["hp_made_priority"] +self.con_value(round(self.hp_made_scale.get()))+","



                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hp_made_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_hp_made_entry(self.data, self.data1)
                    if res == True:
                        self.hp_made_top_level.destroy()
                        self.on_close_hp_made_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hp_made_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.hp_made_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")



                    data = self.work_data["hp_made_amount"].split(',')
                    # removing old amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hp_made_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    data = self.work_data["hp_made_amount"].split(',')
                    data[self.index] = self.hp_made_amount_entry.get()
                    data =",".join(data)
                    self.work_data["hp_made_amount"] = data

                    data = self.work_data["hp_made_app_no"].split(',')
                    data[self.index] = self.hp_made_app_no_var.get()
                    data =",".join(data)
                    self.work_data["hp_made_app_no"] = data

                    data = self.work_data["hp_made_status"].split(',')
                    data[self.index] = self.hp_made_status_var.get()
                    data =",".join(data)
                    self.work_data["hp_made_status"] = data

                    data = self.work_data["hp_made_priority"].split(',')
                    data[self.index] = self.con_value(round(self.hp_made_scale.get()))
                    data =",".join(data)
                    self.work_data["hp_made_priority"] = data
                    # messagebox.showinfo(parent=self.hp_made_top_level,title="",message=data)
                    res = database.com_hp_made_entry(self.data, self.work_data)
                    if res == True:
                        self.hp_made_top_level.destroy()
                        self.on_close_hp_made_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hp_made_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def hp_made_combo_fun(self, event):
        if self.hp_made_combo_box.get() == "NEW ENTRY":
            self.hp_made_amount_var.set("")
            self.hp_made_app_no_var.set("")
            self.hp_made_status_var.set("1")
            self.hp_made_status_change()
            self.hp_made_entry_selection_var = "NEW ENTRY"
            self.hp_made_date_lbl.config(text="")
            self.hp_made_time_lbl.config(text="")
            self.hp_made_scale.set(0)


        # self.data[0]["hp_made_amount"]
        else:
            self.hp_made_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.hp_made_combo_box.get())-1
            amount = self.work_data["hp_made_amount"].split(",")
            app_no = self.work_data["hp_made_app_no"].split(",")
            status = self.work_data["hp_made_status"].split(",")
            date = self.work_data["hp_made_date"].split(",")
            time = self.work_data["hp_made_time"].split(",")
            priority = self.work_data["hp_made_priority"].split(",")
            self.hp_made_amount_var.set(amount[int(self.hp_made_combo_box.get())-1])
            self.hp_made_app_no_var.set(app_no[int(self.hp_made_combo_box.get())-1])
            self.hp_made_status_var.set(status[int(self.hp_made_combo_box.get())-1])
            self.hp_made_date_lbl.config(text=date[int(self.hp_made_combo_box.get())-1])
            self.hp_made_time_lbl.config(text=time[int(self.hp_made_combo_box.get())-1])
            self.hp_made_scale.set(self.con_value_rev(priority[int(self.hp_made_combo_box.get())-1]))
            if self.hp_made_status_var.get() == "0":
                self.hp_made_status_btn.config(image=self.pending_status_img)
            elif self.hp_made_status_var.get() == "1":
                self.hp_made_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.hp_made_top_level, title="",message="")

    def hp_made_entry_delete_fun(self):
        if self.hp_made_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["hp_made_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["hp_made_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_made_amount"] = data

            data = self.work_data["hp_made_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_made_app_no"] = data

            data = self.work_data["hp_made_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_made_status"] = data

            data = self.work_data["hp_made_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_made_date"] = data

            data = self.work_data["hp_made_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_made_time"] = data

            data = self.work_data["hp_made_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hp_made_priority"] = data

            res = database.com_hp_made_entry(self.data, self.work_data)
            if res == True:
                self.hp_made_top_level.destroy()
                self.on_close_hp_made_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.hp_made_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def hp_made_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.hp_made_update_scale_color(value)  # Update scale color based on value

    def convert_hp_made_app_no_to_uppercase(self):
        current_text = self.hp_made_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.hp_made_app_no_var.set(uppercase_text)























    def open_hsrp_win(self):
        if not self.hsrp_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.hsrp_top_level_open = True
            self.hsrp_top_level = Toplevel()
            self.hsrp_top_level.protocol("WM_DELETE_WINDOW", self.on_close_hsrp_top_level)
            self.hsrp_top_level.configure(bg='#B39CD0')
            screen_width = self.hsrp_top_level.winfo_screenwidth()
            screen_height = self.hsrp_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.hsrp_top_level.title("HSRP")
            self.hsrp_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.hsrp_top_level.winfo_screenwidth()
            screen_height = self.hsrp_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.hsrp_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.hsrp_top_level.resizable(False, False)
            self.hsrp_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\hsrp_bg.png"))
            Label(master=self.hsrp_top_level,
                  image=self.hsrp_bg_img).pack()

            self.hsrp_time_lbl = Label(self.hsrp_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.hsrp_time_lbl.place(x=75,y=51)

            self.hsrp_date_lbl = Label(self.hsrp_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.hsrp_date_lbl.place(x=195, y=51)

            self.hsrp_combo_box = ttk.Combobox(self.hsrp_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.hsrp_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.hsrp_scale = ttk.Scale(self.hsrp_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.hsrp_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.hsrp_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["hsrp_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.hsrp_combo_box['values'] = self.combo_values

            self.hsrp_combo_box.bind('<<ComboboxSelected>>', self.hsrp_combo_fun)
            self.hsrp_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.hsrp_amount_var = StringVar()
            self.hsrp_amount_entry = Entry(self.hsrp_top_level,
                                                 textvariable=self.hsrp_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.hsrp_amount_entry.place(x=60, y=125)

            self.hsrp_app_no_var = StringVar()
            self.hsrp_app_no_entry = Entry(self.hsrp_top_level,
                                         textvariable=self.hsrp_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.hsrp_app_no_entry.place(x=60, y=196)
            self.hsrp_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_hsrp_app_no_to_uppercase())

            self.hsrp_status_var = StringVar()
            self.hsrp_status_var.set("0")
            self.hsrp_status_btn = Button(master=self.hsrp_top_level,
                                                textvariable=self.hsrp_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.hsrp_status_change,
                                                borderwidth=0
                                                )
            self.hsrp_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.hsrp_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_hsrp_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.hsrp_top_level,image=self.delete_but_img,
                   command=self.hsrp_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.hsrp_top_level.mainloop()

    def on_close_hsrp_top_level(self):
        self.hsrp_top_level_open = False
        self.hsrp_top_level.destroy()
        self.windows = "closed"

    def hsrp_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def hsrp_status_change(self):
        if self.hsrp_status_var.get() == "0":
            self.hsrp_status_btn.config(image=self.completed_status_img)
            self.hsrp_status_var.set("1")
            print(self.hsrp_status_var.get())
        elif self.hsrp_status_var.get() == "1":
            self.hsrp_status_btn.config(image=self.pending_status_img)
            self.hsrp_status_var.set("0")
            print(self.hsrp_status_var.get())

    def com_hsrp_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.hsrp_priority_var.get()))
        if self.hsrp_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.hsrp_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("hsrp_amount") == None:
                print("1")
                if self.hsrp_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["hsrp_amount"] = self.hsrp_amount_var.get()+","
                    self.data1["hsrp_app_no"] = self.hsrp_app_no_var.get()+","
                    self.data1["hsrp_status"] = self.hsrp_status_var.get()+","
                    self.data1["hsrp_time"] = formatted_time + ","
                    self.data1["hsrp_date"] = formatted_date + ","
                    self.data1["hsrp_priority"] = self.con_value(round(self.hsrp_scale.get()))+","




                    # adding hsrp amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hsrp_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_hsrp_entry(self.data, self.data1)
                    if res == True:
                        self.hsrp_top_level.destroy()
                        self.on_close_hsrp_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hsrp_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("hsrp_amount") != None:
                print("2.0")
                if self.hsrp_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["hsrp_amount"] = self.work_data["hsrp_amount"] +self.hsrp_amount_var.get()+","
                    self.data1["hsrp_app_no"] = self.work_data["hsrp_app_no"] +self.hsrp_app_no_var.get()+","
                    self.data1["hsrp_status"] = self.work_data["hsrp_status"] +self.hsrp_status_var.get()+","
                    self.data1["hsrp_time"] = self.work_data["hsrp_time"] + formatted_time + ","
                    self.data1["hsrp_date"] = self.work_data["hsrp_date"] +formatted_date + ","
                    self.data1["hsrp_priority"] = self.work_data["hsrp_priority"] +self.con_value(round(self.hsrp_scale.get()))+","




                    # adding hsrp amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hsrp_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_hsrp_entry(self.data, self.data1)
                    if res == True:
                        self.hsrp_top_level.destroy()
                        self.on_close_hsrp_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hsrp_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.hsrp_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")



                    data = self.work_data["hsrp_amount"].split(',')
                    # removing old amount of hsrp
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of hsrp
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.hsrp_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    data = self.work_data["hsrp_amount"].split(',')
                    data[self.index] = self.hsrp_amount_entry.get()
                    data =",".join(data)
                    self.work_data["hsrp_amount"] = data

                    data = self.work_data["hsrp_app_no"].split(',')
                    data[self.index] = self.hsrp_app_no_var.get()
                    data =",".join(data)
                    self.work_data["hsrp_app_no"] = data

                    data = self.work_data["hsrp_status"].split(',')
                    data[self.index] = self.hsrp_status_var.get()
                    data =",".join(data)
                    self.work_data["hsrp_status"] = data

                    data = self.work_data["hsrp_priority"].split(',')
                    data[self.index] = self.con_value(round(self.hsrp_scale.get()))
                    data =",".join(data)
                    self.work_data["hsrp_priority"] = data
                    # messagebox.showinfo(parent=self.hsrp_top_level,title="",message=data)
                    res = database.com_hsrp_entry(self.data, self.work_data)
                    if res == True:
                        self.hsrp_top_level.destroy()
                        self.on_close_hsrp_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.hsrp_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def hsrp_combo_fun(self, event):
        if self.hsrp_combo_box.get() == "NEW ENTRY":
            self.hsrp_amount_var.set("")
            self.hsrp_app_no_var.set("")
            self.hsrp_status_var.set("1")
            self.hsrp_status_change()
            self.hsrp_entry_selection_var = "NEW ENTRY"
            self.hsrp_date_lbl.config(text="")
            self.hsrp_time_lbl.config(text="")
            self.hsrp_scale.set(0)


        # self.data[0]["hsrp_amount"]
        else:
            self.hsrp_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.hsrp_combo_box.get())-1
            amount = self.work_data["hsrp_amount"].split(",")
            app_no = self.work_data["hsrp_app_no"].split(",")
            status = self.work_data["hsrp_status"].split(",")
            date = self.work_data["hsrp_date"].split(",")
            time = self.work_data["hsrp_time"].split(",")
            priority = self.work_data["hsrp_priority"].split(",")
            self.hsrp_amount_var.set(amount[int(self.hsrp_combo_box.get())-1])
            self.hsrp_app_no_var.set(app_no[int(self.hsrp_combo_box.get())-1])
            self.hsrp_status_var.set(status[int(self.hsrp_combo_box.get())-1])
            self.hsrp_date_lbl.config(text=date[int(self.hsrp_combo_box.get())-1])
            self.hsrp_time_lbl.config(text=time[int(self.hsrp_combo_box.get())-1])
            self.hsrp_scale.set(self.con_value_rev(priority[int(self.hsrp_combo_box.get())-1]))
            if self.hsrp_status_var.get() == "0":
                self.hsrp_status_btn.config(image=self.pending_status_img)
            elif self.hsrp_status_var.get() == "1":
                self.hsrp_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.hsrp_top_level, title="",message="")

    def hsrp_entry_delete_fun(self):
        if self.hsrp_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)



            # these three line of code, subtract delete work amount from total
            data = self.work_data["hsrp_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])



            data = self.work_data["hsrp_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hsrp_amount"] = data

            data = self.work_data["hsrp_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hsrp_app_no"] = data

            data = self.work_data["hsrp_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hsrp_status"] = data

            data = self.work_data["hsrp_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hsrp_date"] = data

            data = self.work_data["hsrp_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hsrp_time"] = data

            data = self.work_data["hsrp_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["hsrp_priority"] = data

            res = database.com_hsrp_entry(self.data, self.work_data)
            if res == True:
                self.hsrp_top_level.destroy()
                self.on_close_hsrp_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.hsrp_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def hsrp_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.hsrp_update_scale_color(value)  # Update scale color based on value

    def convert_hsrp_app_no_to_uppercase(self):
        current_text = self.hsrp_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.hsrp_app_no_var.set(uppercase_text)





















    def open_fitness_win(self):
        if not self.fitness_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.fitness_top_level_open = True
            self.fitness_top_level = Toplevel()
            self.fitness_top_level.protocol("WM_DELETE_WINDOW", self.on_close_fitness_top_level)
            self.fitness_top_level.configure(bg='#B39CD0')
            screen_width = self.fitness_top_level.winfo_screenwidth()
            screen_height = self.fitness_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.fitness_top_level.title("FITNESS")
            self.fitness_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.fitness_top_level.winfo_screenwidth()
            screen_height = self.fitness_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.fitness_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.fitness_top_level.resizable(False, False)
            self.fitness_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\fitness_bg.png"))
            Label(master=self.fitness_top_level,
                  image=self.fitness_bg_img).pack()

            self.fitness_time_lbl = Label(self.fitness_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.fitness_time_lbl.place(x=75,y=51)

            self.fitness_date_lbl = Label(self.fitness_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.fitness_date_lbl.place(x=195, y=51)

            self.fitness_combo_box = ttk.Combobox(self.fitness_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.fitness_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.fitness_scale = ttk.Scale(self.fitness_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.fitness_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.fitness_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["fitness_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.fitness_combo_box['values'] = self.combo_values

            self.fitness_combo_box.bind('<<ComboboxSelected>>', self.fitness_combo_fun)
            self.fitness_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.fitness_amount_var = StringVar()
            self.fitness_amount_entry = Entry(self.fitness_top_level,
                                                 textvariable=self.fitness_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.fitness_amount_entry.place(x=60, y=125)

            self.fitness_app_no_var = StringVar()
            self.fitness_app_no_entry = Entry(self.fitness_top_level,
                                         textvariable=self.fitness_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.fitness_app_no_entry.place(x=60, y=196)
            self.fitness_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_fitness_app_no_to_uppercase())

            self.fitness_status_var = StringVar()
            self.fitness_status_var.set("0")
            self.fitness_status_btn = Button(master=self.fitness_top_level,
                                                textvariable=self.fitness_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.fitness_status_change,
                                                borderwidth=0
                                                )
            self.fitness_status_btn.place(x=250, y=125)

            self.fitness_expiry_date_var = StringVar()
            self.fitness_expiry_date_entry = DateEntry(self.fitness_top_level,
                                                        textvariable=self.fitness_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 2,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.fitness_expiry_date_entry.place(x=325, y=200)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.fitness_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_fitness_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.fitness_top_level,image=self.delete_but_img,
                   command=self.fitness_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.fitness_top_level.mainloop()

    def on_close_fitness_top_level(self):
        self.fitness_top_level_open = False
        self.fitness_top_level.destroy()
        self.windows = "closed"

    def fitness_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def fitness_status_change(self):
        if self.fitness_status_var.get() == "0":
            self.fitness_status_btn.config(image=self.completed_status_img)
            self.fitness_status_var.set("1")
            print(self.fitness_status_var.get())
        elif self.fitness_status_var.get() == "1":
            self.fitness_status_btn.config(image=self.pending_status_img)
            self.fitness_status_var.set("0")
            print(self.fitness_status_var.get())

    def con_value(self, value):
        # coverting value
        # Dictionary mapping values to their corresponding strings
        value_map = {0: "l", 1: "m", 2: "h"}
        return value_map.get(value, None)

    def con_value_rev(self, value):
        # coverting value vice versa

        # Dictionary mapping values to their corresponding strings
        value_map = {"l": 0, "m": 1, "h": 2}
        return value_map.get(value, None)
    def com_fitness_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.fitness_priority_var.get()))
        if self.fitness_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.fitness_top_level)
        elif self.fitness_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.fitness_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("fitness_amount") == None:
                print("1")
                if self.fitness_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["fitness_amount"] = self.fitness_amount_var.get()+","
                    self.data1["fitness_app_no"] = self.fitness_app_no_var.get()+","
                    self.data1["fitness_status"] = self.fitness_status_var.get()+","
                    self.data1["fitness_time"] = formatted_time + ","
                    self.data1["fitness_date"] = formatted_date + ","
                    self.data1["fitness_priority"] = self.con_value(round(self.fitness_scale.get()))+","
                    self.data1["fitness_expiry_date"] = self.fitness_expiry_date_var.get()+","




                    # adding fitness amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.fitness_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_fitness_entry(self.data, self.data1)
                    if res == True:
                        self.fitness_top_level.destroy()
                        self.on_close_fitness_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.fitness_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("fitness_amount") != None:
                print("2.0")
                if self.fitness_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["fitness_amount"] = self.work_data["fitness_amount"] +self.fitness_amount_var.get()+","
                    self.data1["fitness_app_no"] = self.work_data["fitness_app_no"] +self.fitness_app_no_var.get()+","
                    self.data1["fitness_status"] = self.work_data["fitness_status"] +self.fitness_status_var.get()+","
                    self.data1["fitness_time"] = self.work_data["fitness_time"] + formatted_time + ","
                    self.data1["fitness_date"] = self.work_data["fitness_date"] +formatted_date + ","
                    self.data1["fitness_priority"] = self.work_data["fitness_priority"] +self.con_value(round(self.fitness_scale.get()))+","
                    self.data1["fitness_expiry_date"] = self.work_data["fitness_expiry_date"] +self.fitness_expiry_date_var.get()+","



                    # adding fitness amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.fitness_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_fitness_entry(self.data, self.data1)
                    if res == True:
                        self.fitness_top_level.destroy()
                        self.on_close_fitness_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.fitness_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.fitness_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["fitness_amount"].split(',')
                    # removing old amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.fitness_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["fitness_amount"].split(',')
                    data[self.index] = self.fitness_amount_entry.get()
                    data =",".join(data)
                    self.work_data["fitness_amount"] = data

                    data = self.work_data["fitness_app_no"].split(',')
                    data[self.index] = self.fitness_app_no_var.get()
                    data =",".join(data)
                    self.work_data["fitness_app_no"] = data

                    data = self.work_data["fitness_status"].split(',')
                    data[self.index] = self.fitness_status_var.get()
                    data =",".join(data)
                    self.work_data["fitness_status"] = data

                    data = self.work_data["fitness_priority"].split(',')
                    data[self.index] = self.con_value(round(self.fitness_scale.get()))
                    data =",".join(data)
                    self.work_data["fitness_priority"] = data

                    data = self.work_data["fitness_expiry_date"].split(',')
                    data[self.index] = self.fitness_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["fitness_expiry_date"] = data
                    # messagebox.showinfo(parent=self.fitness_top_level,title="",message=data)
                    res = database.com_fitness_entry(self.data, self.work_data)
                    if res == True:
                        self.fitness_top_level.destroy()
                        self.on_close_fitness_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.fitness_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def fitness_combo_fun(self, event):
        if self.fitness_combo_box.get() == "NEW ENTRY":
            self.fitness_amount_var.set("")
            self.fitness_app_no_var.set("")
            self.fitness_status_var.set("1")
            self.fitness_status_change()
            self.fitness_entry_selection_var = "NEW ENTRY"
            self.fitness_date_lbl.config(text="")
            self.fitness_time_lbl.config(text="")
            self.fitness_scale.set(0)
            self.fitness_expiry_date_var.set("")


        # self.data[0]["fitness_amount"]
        else:
            self.fitness_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.fitness_combo_box.get())-1
            amount = self.work_data["fitness_amount"].split(",")
            app_no = self.work_data["fitness_app_no"].split(",")
            status = self.work_data["fitness_status"].split(",")
            date = self.work_data["fitness_date"].split(",")
            time = self.work_data["fitness_time"].split(",")
            priority = self.work_data["fitness_priority"].split(",")
            print(priority)
            fitness_expiry = self.work_data["fitness_expiry_date"].split(",")
            self.fitness_amount_var.set(amount[int(self.fitness_combo_box.get())-1])
            self.fitness_app_no_var.set(app_no[int(self.fitness_combo_box.get())-1])
            self.fitness_status_var.set(status[int(self.fitness_combo_box.get())-1])
            self.fitness_date_lbl.config(text=date[int(self.fitness_combo_box.get())-1])
            self.fitness_time_lbl.config(text=time[int(self.fitness_combo_box.get())-1])
            self.fitness_scale.set(self.con_value_rev(priority[int(self.fitness_combo_box.get())-1]))
            print(self.fitness_scale.get())
            self.fitness_expiry_date_var.set(fitness_expiry[int(self.fitness_combo_box.get())-1])
            if self.fitness_status_var.get() == "0":
                self.fitness_status_btn.config(image=self.pending_status_img)
            elif self.fitness_status_var.get() == "1":
                self.fitness_status_btn.config(image=self.completed_status_img)

    def fitness_entry_delete_fun(self):
        if self.fitness_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)



            # these three line of code, subtract delete work amount from total
            data = self.work_data["fitness_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])



            data = self.work_data["fitness_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fitness_amount"] = data

            data = self.work_data["fitness_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fitness_app_no"] = data

            data = self.work_data["fitness_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fitness_status"] = data

            data = self.work_data["fitness_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fitness_date"] = data

            data = self.work_data["fitness_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fitness_time"] = data

            data = self.work_data["fitness_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fitness_priority"] = data

            data = self.work_data["fitness_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fitness_expiry_date"] = data

            res = database.com_fitness_entry(self.data, self.work_data)
            if res == True:
                self.fitness_top_level.destroy()
                self.on_close_fitness_top_level()
                self.update_data(self.all_data, self.data[0])
            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.fitness_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def fitness_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.fitness_update_scale_color(value)  # Update scale color based on value

    def convert_fitness_app_no_to_uppercase(self):
        current_text = self.fitness_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.fitness_app_no_var.set(uppercase_text)

















    def open_insurance_win(self):
        if not self.insurance_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.insurance_top_level_open = True
            self.insurance_top_level = Toplevel()
            self.insurance_top_level.protocol("WM_DELETE_WINDOW", self.on_close_insurance_top_level)
            self.insurance_top_level.configure(bg='#B39CD0')
            screen_width = self.insurance_top_level.winfo_screenwidth()
            screen_height = self.insurance_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.insurance_top_level.title("INSURANCE")
            self.insurance_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.insurance_top_level.winfo_screenwidth()
            screen_height = self.insurance_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.insurance_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.insurance_top_level.resizable(False, False)
            self.insurance_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\insurance_bg.png"))
            Label(master=self.insurance_top_level,
                  image=self.insurance_bg_img).pack()

            self.insurance_time_lbl = Label(self.insurance_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.insurance_time_lbl.place(x=75,y=51)

            self.insurance_date_lbl = Label(self.insurance_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.insurance_date_lbl.place(x=195, y=51)

            self.insurance_combo_box = ttk.Combobox(self.insurance_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.insurance_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.insurance_scale = ttk.Scale(self.insurance_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.insurance_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.insurance_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["insurance_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.insurance_combo_box['values'] = self.combo_values

            self.insurance_combo_box.bind('<<ComboboxSelected>>', self.insurance_combo_fun)
            self.insurance_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.insurance_amount_var = StringVar()
            self.insurance_amount_entry = Entry(self.insurance_top_level,
                                                 textvariable=self.insurance_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.insurance_amount_entry.place(x=60, y=125)




            self.insurance_status_var = StringVar()
            self.insurance_status_var.set("0")
            self.insurance_status_btn = Button(master=self.insurance_top_level,
                                                textvariable=self.insurance_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.insurance_status_change,
                                                borderwidth=0
                                                )
            self.insurance_status_btn.place(x=250, y=125)

            self.insurance_expiry_date_var = StringVar()
            self.insurance_expiry_date_entry = DateEntry(self.insurance_top_level,
                                                        textvariable=self.insurance_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 1,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.insurance_expiry_date_entry.place(x=325, y=200)

            self.insurance_discount_var = StringVar()
            self.insurance_discount_entry = Entry(self.insurance_top_level,
                                                  textvariable=self.insurance_discount_var,
                                                  bg=self.color_1,
                                                  border=0,
                                                  # state="disabled",
                                                  # disabledbackground=self.color_1,
                                                  validate="key",
                                                  validatecommand=(self.main_root.register(self.validate_amount),
                                                                   "%P"),
                                                  width=self.field_width_2,
                                                  font=("Helvetica", self.font_size))
            self.insurance_discount_entry.place(x=60, y=196)

            self.insurance_app_no_var = StringVar()
            self.insurance_app_no_entry = Entry(self.insurance_top_level,
                                         textvariable=self.insurance_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.insurance_app_no_entry.place(x=60, y=266)
            self.insurance_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_insurance_app_no_to_uppercase())

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.insurance_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_insurance_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.insurance_top_level,image=self.delete_but_img,
                   command=self.insurance_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.insurance_top_level.mainloop()

    def on_close_insurance_top_level(self):
        self.insurance_top_level_open = False
        self.insurance_top_level.destroy()
        self.windows = "closed"

    def insurance_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[( f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def insurance_status_change(self):
        if self.insurance_status_var.get() == "0":
            self.insurance_status_btn.config(image=self.completed_status_img)
            self.insurance_status_var.set("1")
            print(self.insurance_status_var.get())
        elif self.insurance_status_var.get() == "1":
            self.insurance_status_btn.config(image=self.pending_status_img)
            self.insurance_status_var.set("0")
            print(self.insurance_status_var.get())

    def com_insurance_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.insurance_priority_var.get()))
        if self.insurance_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.insurance_top_level)
        elif self.insurance_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.insurance_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("insurance_amount") == None:
                print("1")
                if self.insurance_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["insurance_amount"] = self.insurance_amount_var.get()+","
                    self.data1["insurance_app_no"] = self.insurance_app_no_var.get()+","
                    self.data1["insurance_status"] = self.insurance_status_var.get()+","
                    self.data1["insurance_time"] = formatted_time + ","
                    self.data1["insurance_date"] = formatted_date + ","
                    self.data1["insurance_priority"] = self.con_value(round(self.insurance_scale.get()))+","
                    self.data1["insurance_expiry_date"] = self.insurance_expiry_date_var.get()+","
                    self.data1["insurance_discount_var"] = self.insurance_discount_var.get()+","




                    # adding insurance amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.insurance_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_insurance_entry(self.data, self.data1)
                    if res == True:
                        self.insurance_top_level.destroy()
                        self.on_close_insurance_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.insurance_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("insurance_amount") != None:
                print("2.0")
                if self.insurance_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["insurance_amount"] = self.work_data["insurance_amount"] +self.insurance_amount_var.get()+","
                    self.data1["insurance_app_no"] = self.work_data["insurance_app_no"] +self.insurance_app_no_var.get()+","
                    self.data1["insurance_status"] = self.work_data["insurance_status"] +self.insurance_status_var.get()+","
                    self.data1["insurance_time"] = self.work_data["insurance_time"] + formatted_time + ","
                    self.data1["insurance_date"] = self.work_data["insurance_date"] +formatted_date + ","
                    self.data1["insurance_priority"] = self.work_data["insurance_priority"] +self.con_value(round(self.insurance_scale.get()))+","
                    self.data1["insurance_expiry_date"] = self.work_data["insurance_expiry_date"] +self.insurance_expiry_date_var.get()+","
                    self.data1["insurance_discount_var"] = self.work_data["insurance_discount_var"] +self.insurance_discount_var.get()+","




                    # adding insurance amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.insurance_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_insurance_entry(self.data, self.data1)
                    if res == True:
                        self.insurance_top_level.destroy()
                        self.on_close_insurance_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.insurance_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.insurance_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")



                    data = self.work_data["insurance_amount"].split(',')
                    # removing old amount of insurance
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of insurance
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.insurance_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    data = self.work_data["insurance_amount"].split(',')
                    data[self.index] = self.insurance_amount_entry.get()
                    data =",".join(data)
                    self.work_data["insurance_amount"] = data

                    data = self.work_data["insurance_app_no"].split(',')
                    data[self.index] = self.insurance_app_no_var.get()
                    data =",".join(data)
                    self.work_data["insurance_app_no"] = data

                    data = self.work_data["insurance_status"].split(',')
                    data[self.index] = self.insurance_status_var.get()
                    data =",".join(data)
                    self.work_data["insurance_status"] = data

                    data = self.work_data["insurance_priority"].split(',')
                    data[self.index] = self.con_value(round(self.insurance_scale.get()))
                    data =",".join(data)
                    self.work_data["insurance_priority"] = data

                    data = self.work_data["insurance_expiry_date"].split(',')
                    data[self.index] = self.insurance_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["insurance_expiry_date"] = data

                    data = self.work_data["insurance_discount_var"].split(',')
                    data[self.index] = self.insurance_discount_var.get()
                    data =",".join(data)
                    self.work_data["insurance_discount_var"] = data
                    # messagebox.showinfo(parent=self.insurance_top_level,title="",message=data)
                    res = database.com_insurance_entry(self.data, self.work_data)
                    if res == True:
                        self.insurance_top_level.destroy()
                        self.on_close_insurance_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.insurance_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def insurance_combo_fun(self, event):
        if self.insurance_combo_box.get() == "NEW ENTRY":
            self.insurance_amount_var.set("")
            self.insurance_app_no_var.set("")
            self.insurance_status_var.set("1")
            self.insurance_status_change()
            self.insurance_entry_selection_var = "NEW ENTRY"
            self.insurance_date_lbl.config(text="")
            self.insurance_time_lbl.config(text="")
            self.insurance_scale.set(0)
            self.insurance_expiry_date_var.set("")
            self.insurance_discount_var.set("")

        # self.data[0]["insurance_amount"]
        else:
            self.insurance_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.insurance_combo_box.get())-1
            amount = self.work_data["insurance_amount"].split(",")
            app_no = self.work_data["insurance_app_no"].split(",")
            status = self.work_data["insurance_status"].split(",")
            date = self.work_data["insurance_date"].split(",")
            time = self.work_data["insurance_time"].split(",")
            priority = self.work_data["insurance_priority"].split(",")
            insurance_expiry = self.work_data["insurance_expiry_date"].split(",")
            insurance_discount = self.work_data["insurance_discount_var"].split(",")
            self.insurance_amount_var.set(amount[int(self.insurance_combo_box.get())-1])
            self.insurance_app_no_var.set(app_no[int(self.insurance_combo_box.get())-1])
            self.insurance_status_var.set(status[int(self.insurance_combo_box.get())-1])
            self.insurance_date_lbl.config(text=date[int(self.insurance_combo_box.get())-1])
            self.insurance_time_lbl.config(text=time[int(self.insurance_combo_box.get())-1])
            self.insurance_scale.set(self.con_value_rev(priority[int(self.insurance_combo_box.get())-1]))
            self.insurance_expiry_date_var.set(insurance_expiry[int(self.insurance_combo_box.get())-1])
            self.insurance_discount_var.set(insurance_discount[int(self.insurance_combo_box.get())-1])
            if self.insurance_status_var.get() == "0":
                self.insurance_status_btn.config(image=self.pending_status_img)
            elif self.insurance_status_var.get() == "1":
                self.insurance_status_btn.config(image=self.completed_status_img)

    def insurance_entry_delete_fun(self):
        if self.insurance_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)



            # these three line of code, subtract delete work amount from total
            data = self.work_data["insurance_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["insurance_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_amount"] = data

            data = self.work_data["insurance_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_app_no"] = data


            data = self.work_data["insurance_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_status"] = data

            data = self.work_data["insurance_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_date"] = data

            data = self.work_data["insurance_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_time"] = data

            data = self.work_data["insurance_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_priority"] = data

            data = self.work_data["insurance_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_expiry_date"] = data

            data = self.work_data["insurance_discount_var"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["insurance_discount_var"] = data
            res = database.com_insurance_entry(self.data, self.work_data)
            if res == True:
                self.insurance_top_level.destroy()
                self.on_close_insurance_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.insurance_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def insurance_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.insurance_update_scale_color(value)  # Update scale color based on value

    def convert_insurance_app_no_to_uppercase(self):
        current_text = self.insurance_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.insurance_app_no_var.set(uppercase_text)






















    def open_pb_late_fine_win(self):
        if not self.pb_late_fine_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.pb_late_fine_top_level_open = True
            self.pb_late_fine_top_level = Toplevel()
            self.pb_late_fine_top_level.protocol("WM_DELETE_WINDOW", self.on_close_pb_late_fine_top_level)
            self.pb_late_fine_top_level.configure(bg='#B39CD0')
            screen_width = self.pb_late_fine_top_level.winfo_screenwidth()
            screen_height = self.pb_late_fine_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.pb_late_fine_top_level.title("PB LATE FINE")
            self.pb_late_fine_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.pb_late_fine_top_level.winfo_screenwidth()
            screen_height = self.pb_late_fine_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.pb_late_fine_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.pb_late_fine_top_level.resizable(False, False)
            self.pb_late_fine_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\pb_late_fine_bg.png"))
            Label(master=self.pb_late_fine_top_level,
                  image=self.pb_late_fine_bg_img).pack()

            self.pb_late_fine_time_lbl = Label(self.pb_late_fine_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.pb_late_fine_time_lbl.place(x=75,y=51)

            self.pb_late_fine_date_lbl = Label(self.pb_late_fine_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.pb_late_fine_date_lbl.place(x=195, y=51)

            self.pb_late_fine_combo_box = ttk.Combobox(self.pb_late_fine_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.pb_late_fine_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.pb_late_fine_scale = ttk.Scale(self.pb_late_fine_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.pb_late_fine_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.pb_late_fine_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["pb_late_fine_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.pb_late_fine_combo_box['values'] = self.combo_values

            self.pb_late_fine_combo_box.bind('<<ComboboxSelected>>', self.pb_late_fine_combo_fun)
            self.pb_late_fine_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.pb_late_fine_amount_var = StringVar()
            self.pb_late_fine_amount_entry = Entry(self.pb_late_fine_top_level,
                                                 textvariable=self.pb_late_fine_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.pb_late_fine_amount_entry.place(x=60, y=125)


            self.pb_late_fine_app_no_var = StringVar()
            self.pb_late_fine_app_no_entry = Entry(self.pb_late_fine_top_level,
                                         textvariable=self.pb_late_fine_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.pb_late_fine_app_no_entry.place(x=60, y=196)
            self.pb_late_fine_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_pb_late_fine_app_no_to_uppercase())

            self.pb_late_fine_expiry_date_var = StringVar()
            self.pb_late_fine_expiry_date_entry = DateEntry(self.pb_late_fine_top_level,
                                                        textvariable=self.pb_late_fine_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 1,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.pb_late_fine_expiry_date_entry.place(x=325, y=200)
            self.pb_late_fine_status_var = StringVar()
            self.pb_late_fine_status_var.set("0")
            self.pb_late_fine_status_btn = Button(master=self.pb_late_fine_top_level,
                                                textvariable=self.pb_late_fine_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.pb_late_fine_status_change,
                                                borderwidth=0
                                                )
            self.pb_late_fine_status_btn.place(x=250, y=125)



            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.pb_late_fine_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_pb_late_fine_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.pb_late_fine_top_level,image=self.delete_but_img,
                   command=self.pb_late_fine_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.pb_late_fine_top_level.mainloop()

    def on_close_pb_late_fine_top_level(self):
        self.pb_late_fine_top_level_open = False
        self.pb_late_fine_top_level.destroy()
        self.windows = "closed"

    def pb_late_fine_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def pb_late_fine_status_change(self):
        if self.pb_late_fine_status_var.get() == "0":
            self.pb_late_fine_status_btn.config(image=self.completed_status_img)
            self.pb_late_fine_status_var.set("1")
            print(self.pb_late_fine_status_var.get())
        elif self.pb_late_fine_status_var.get() == "1":
            self.pb_late_fine_status_btn.config(image=self.pending_status_img)
            self.pb_late_fine_status_var.set("0")
            print(self.pb_late_fine_status_var.get())

    def com_pb_late_fine_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.pb_late_fine_priority_var.get()))
        if self.pb_late_fine_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.pb_late_fine_top_level)
        elif self.pb_late_fine_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.pb_late_fine_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("pb_late_fine_amount") == None:
                print("1")
                if self.pb_late_fine_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["pb_late_fine_amount"] = self.pb_late_fine_amount_var.get()+","
                    self.data1["pb_late_fine_app_no"] = self.pb_late_fine_app_no_var.get()+","
                    self.data1["pb_late_fine_status"] = self.pb_late_fine_status_var.get()+","
                    self.data1["pb_late_fine_time"] = formatted_time + ","
                    self.data1["pb_late_fine_date"] = formatted_date + ","
                    self.data1["pb_late_fine_priority"] = self.con_value(round(self.pb_late_fine_scale.get()))+","
                    self.data1["pb_late_fine_expiry_date"] = self.pb_late_fine_expiry_date_var.get()+","




                    # adding pb late amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_late_fine_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_pb_late_fine_entry(self.data, self.data1)
                    if res == True:
                        self.pb_late_fine_top_level.destroy()
                        self.on_close_pb_late_fine_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_late_fine_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("pb_late_fine_amount") != None:
                print("2.0")
                if self.pb_late_fine_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["pb_late_fine_amount"] = self.work_data["pb_late_fine_amount"] +self.pb_late_fine_amount_var.get()+","
                    self.data1["pb_late_fine_app_no"] = self.work_data["pb_late_fine_app_no"] +self.pb_late_fine_app_no_var.get()+","
                    self.data1["pb_late_fine_status"] = self.work_data["pb_late_fine_status"] +self.pb_late_fine_status_var.get()+","
                    self.data1["pb_late_fine_time"] = self.work_data["pb_late_fine_time"] + formatted_time + ","
                    self.data1["pb_late_fine_date"] = self.work_data["pb_late_fine_date"] +formatted_date + ","
                    self.data1["pb_late_fine_priority"] = self.work_data["pb_late_fine_priority"] +self.con_value(round(self.pb_late_fine_scale.get()))+","
                    self.data1["pb_late_fine_expiry_date"] = self.work_data["pb_late_fine_expiry_date"] +self.pb_late_fine_expiry_date_var.get()+","




                    # adding pb late amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_late_fine_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_pb_late_fine_entry(self.data, self.data1)
                    if res == True:
                        self.pb_late_fine_top_level.destroy()
                        self.on_close_pb_late_fine_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_late_fine_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.pb_late_fine_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["pb_late_fine_amount"].split(',')
                    # removing old amount of pb_late_fine
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of pb_late_fine
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_late_fine_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["pb_late_fine_amount"].split(',')
                    data[self.index] = self.pb_late_fine_amount_entry.get()
                    data =",".join(data)
                    self.work_data["pb_late_fine_amount"] = data

                    data = self.work_data["pb_late_fine_app_no"].split(',')
                    data[self.index] = self.pb_late_fine_app_no_var.get()
                    data =",".join(data)
                    self.work_data["pb_late_fine_app_no"] = data

                    data = self.work_data["pb_late_fine_status"].split(',')
                    data[self.index] = self.pb_late_fine_status_var.get()
                    data =",".join(data)
                    self.work_data["pb_late_fine_status"] = data

                    data = self.work_data["pb_late_fine_priority"].split(',')
                    data[self.index] = self.con_value(round(self.pb_late_fine_scale.get()))
                    data =",".join(data)
                    self.work_data["pb_late_fine_priority"] = data

                    data = self.work_data["pb_late_fine_expiry_date"].split(',')
                    data[self.index] = self.pb_late_fine_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["pb_late_fine_expiry_date"] = data
                    # messagebox.showinfo(parent=self.pb_late_fine_top_level,title="",message=data)
                    res = database.com_pb_late_fine_entry(self.data, self.work_data)
                    if res == True:
                        self.pb_late_fine_top_level.destroy()
                        self.on_close_pb_late_fine_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_late_fine_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def pb_late_fine_combo_fun(self, event):
        if self.pb_late_fine_combo_box.get() == "NEW ENTRY":
            self.pb_late_fine_amount_var.set("")
            self.pb_late_fine_app_no_var.set("")
            self.pb_late_fine_status_var.set("1")
            self.pb_late_fine_status_change()
            self.pb_late_fine_entry_selection_var = "NEW ENTRY"
            self.pb_late_fine_date_lbl.config(text="")
            self.pb_late_fine_time_lbl.config(text="")
            self.pb_late_fine_scale.set(0)
            self.pb_late_fine_expiry_date_var.set("")


        # self.data[0]["pb_late_fine_amount"]
        else:
            self.pb_late_fine_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.pb_late_fine_combo_box.get())-1
            amount = self.work_data["pb_late_fine_amount"].split(",")
            app_no = self.work_data["pb_late_fine_app_no"].split(",")
            status = self.work_data["pb_late_fine_status"].split(",")
            date = self.work_data["pb_late_fine_date"].split(",")
            time = self.work_data["pb_late_fine_time"].split(",")
            priority = self.work_data["pb_late_fine_priority"].split(",")
            pb_late_fine_expiry = self.work_data["pb_late_fine_expiry_date"].split(",")
            self.pb_late_fine_amount_var.set(amount[int(self.pb_late_fine_combo_box.get())-1])
            self.pb_late_fine_app_no_var.set(app_no[int(self.pb_late_fine_combo_box.get())-1])
            self.pb_late_fine_status_var.set(status[int(self.pb_late_fine_combo_box.get())-1])
            self.pb_late_fine_date_lbl.config(text=date[int(self.pb_late_fine_combo_box.get())-1])
            self.pb_late_fine_time_lbl.config(text=time[int(self.pb_late_fine_combo_box.get())-1])
            self.pb_late_fine_scale.set(self.con_value_rev(priority[int(self.pb_late_fine_combo_box.get())-1]))
            self.pb_late_fine_expiry_date_var.set(pb_late_fine_expiry[int(self.pb_late_fine_combo_box.get())-1])
            if self.pb_late_fine_status_var.get() == "0":
                self.pb_late_fine_status_btn.config(image=self.pending_status_img)
            elif self.pb_late_fine_status_var.get() == "1":
                self.pb_late_fine_status_btn.config(image=self.completed_status_img)

    def pb_late_fine_entry_delete_fun(self):
        if self.pb_late_fine_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)



            # these three line of code, subtract delete work amount from total
            data = self.work_data["pb_late_fine_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["pb_late_fine_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_late_fine_amount"] = data

            data = self.work_data["pb_late_fine_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_late_fine_app_no"] = data

            data = self.work_data["pb_late_fine_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_late_fine_status"] = data

            data = self.work_data["pb_late_fine_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_late_fine_date"] = data

            data = self.work_data["pb_late_fine_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_late_fine_time"] = data

            data = self.work_data["pb_late_fine_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_late_fine_priority"] = data

            data = self.work_data["pb_late_fine_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_late_fine_expiry_date"] = data

            res = database.com_pb_late_fine_entry(self.data, self.work_data)
            if res == True:
                self.pb_late_fine_top_level.destroy()
                self.on_close_pb_late_fine_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.pb_late_fine_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def pb_late_fine_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.pb_late_fine_update_scale_color(value)  # Update scale color based on value

    def convert_pb_late_fine_app_no_to_uppercase(self):
        current_text = self.pb_late_fine_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.pb_late_fine_app_no_var.set(uppercase_text)


















    def open_np_late_fine_win(self):
        if not self.np_late_fine_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.np_late_fine_top_level_open = True
            self.np_late_fine_top_level = Toplevel()
            self.np_late_fine_top_level.protocol("WM_DELETE_WINDOW", self.on_close_np_late_fine_top_level)
            self.np_late_fine_top_level.configure(bg='#B39CD0')
            screen_width = self.np_late_fine_top_level.winfo_screenwidth()
            screen_height = self.np_late_fine_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.np_late_fine_top_level.title("NP LATE FINE")
            self.np_late_fine_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.np_late_fine_top_level.winfo_screenwidth()
            screen_height = self.np_late_fine_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.np_late_fine_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.np_late_fine_top_level.resizable(False, False)
            self.np_late_fine_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\np_late_fine_bg.png"))
            Label(master=self.np_late_fine_top_level,
                  image=self.np_late_fine_bg_img).pack()

            self.np_late_fine_time_lbl = Label(self.np_late_fine_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.np_late_fine_time_lbl.place(x=75,y=51)

            self.np_late_fine_date_lbl = Label(self.np_late_fine_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.np_late_fine_date_lbl.place(x=195, y=51)

            self.np_late_fine_combo_box = ttk.Combobox(self.np_late_fine_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.np_late_fine_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.np_late_fine_scale = ttk.Scale(self.np_late_fine_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.np_late_fine_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.np_late_fine_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["np_late_fine_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.np_late_fine_combo_box['values'] = self.combo_values

            self.np_late_fine_combo_box.bind('<<ComboboxSelected>>', self.np_late_fine_combo_fun)
            self.np_late_fine_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.np_late_fine_amount_var = StringVar()
            self.np_late_fine_amount_entry = Entry(self.np_late_fine_top_level,
                                                 textvariable=self.np_late_fine_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.np_late_fine_amount_entry.place(x=60, y=125)

            self.np_late_fine_app_no_var = StringVar()
            self.np_late_fine_app_no_entry = Entry(self.np_late_fine_top_level,
                                         textvariable=self.np_late_fine_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.np_late_fine_app_no_entry.place(x=60, y=196)
            self.np_late_fine_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_np_late_fine_app_no_to_uppercase())

            self.np_late_fine_expiry_date_var = StringVar()
            self.np_late_fine_expiry_date_entry = DateEntry(self.np_late_fine_top_level,
                                                        textvariable=self.np_late_fine_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 1,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.np_late_fine_expiry_date_entry.place(x=325, y=200)
            self.np_late_fine_status_var = StringVar()
            self.np_late_fine_status_var.set("0")
            self.np_late_fine_status_btn = Button(master=self.np_late_fine_top_level,
                                                textvariable=self.np_late_fine_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.np_late_fine_status_change,
                                                borderwidth=0
                                                )
            self.np_late_fine_status_btn.place(x=250, y=125)



            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.np_late_fine_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_np_late_fine_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.np_late_fine_top_level,image=self.delete_but_img,
                   command=self.np_late_fine_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.np_late_fine_top_level.mainloop()

    def on_close_np_late_fine_top_level(self):
        self.np_late_fine_top_level_open = False
        self.np_late_fine_top_level.destroy()
        self.windows = "closed"

    def np_late_fine_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def np_late_fine_status_change(self):
        if self.np_late_fine_status_var.get() == "0":
            self.np_late_fine_status_btn.config(image=self.completed_status_img)
            self.np_late_fine_status_var.set("1")
            print(self.np_late_fine_status_var.get())
        elif self.np_late_fine_status_var.get() == "1":
            self.np_late_fine_status_btn.config(image=self.pending_status_img)
            self.np_late_fine_status_var.set("0")
            print(self.np_late_fine_status_var.get())

    def com_np_late_fine_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.np_late_fine_priority_var.get()))
        if self.np_late_fine_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.np_late_fine_top_level)
        elif self.np_late_fine_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.np_late_fine_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("np_late_fine_amount") == None:
                print("1")
                if self.np_late_fine_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["np_late_fine_amount"] = self.np_late_fine_amount_var.get()+","
                    self.data1["np_late_fine_app_no"] = self.np_late_fine_app_no_var.get()+","
                    self.data1["np_late_fine_status"] = self.np_late_fine_status_var.get()+","
                    self.data1["np_late_fine_time"] = formatted_time + ","
                    self.data1["np_late_fine_date"] = formatted_date + ","
                    self.data1["np_late_fine_priority"] = self.con_value(round(self.np_late_fine_scale.get()))+","
                    self.data1["np_late_fine_expiry_date"] = self.np_late_fine_expiry_date_var.get()+","





                    # adding np_late_fine amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_late_fine_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_np_late_fine_entry(self.data,self.data1)
                    if res == True:
                        self.np_late_fine_top_level.destroy()
                        self.on_close_np_late_fine_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_late_fine_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("np_late_fine_amount") != None:
                print("2.0")
                if self.np_late_fine_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["np_late_fine_amount"] = self.work_data["np_late_fine_amount"] +self.np_late_fine_amount_var.get()+","
                    self.data1["np_late_fine_app_no"] = self.work_data["np_late_fine_app_no"] +self.np_late_fine_app_no_var.get()+","
                    self.data1["np_late_fine_status"] = self.work_data["np_late_fine_status"] +self.np_late_fine_status_var.get()+","
                    self.data1["np_late_fine_time"] = self.work_data["np_late_fine_time"] + formatted_time + ","
                    self.data1["np_late_fine_date"] = self.work_data["np_late_fine_date"] +formatted_date + ","
                    self.data1["np_late_fine_priority"] = self.work_data["np_late_fine_priority"] +self.con_value(round(self.np_late_fine_scale.get()))+","
                    self.data1["np_late_fine_expiry_date"] = self.work_data["np_late_fine_expiry_date"] +self.np_late_fine_expiry_date_var.get()+","




                    # adding np_late_fine amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_late_fine_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_np_late_fine_entry(self.data, self.data1)
                    if res == True:
                        self.np_late_fine_top_level.destroy()
                        self.on_close_np_late_fine_top_level()
                        self.update_data(self.all_data, self.data[0])
                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_late_fine_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.np_late_fine_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")



                    data = self.work_data["np_late_fine_amount"].split(',')
                    # removing old amount of np_late_fine
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of np_late_fine
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_late_fine_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    data = self.work_data["np_late_fine_amount"].split(',')
                    data[self.index] = self.np_late_fine_amount_entry.get()
                    data =",".join(data)
                    self.work_data["np_late_fine_amount"] = data

                    data = self.work_data["np_late_fine_app_no"].split(',')
                    data[self.index] = self.np_late_fine_app_no_var.get()
                    data =",".join(data)
                    self.work_data["np_late_fine_app_no"] = data

                    data = self.work_data["np_late_fine_status"].split(',')
                    data[self.index] = self.np_late_fine_status_var.get()
                    data =",".join(data)
                    self.work_data["np_late_fine_status"] = data

                    data = self.work_data["np_late_fine_priority"].split(',')
                    data[self.index] = self.con_value(round(self.np_late_fine_scale.get()))
                    data =",".join(data)
                    self.work_data["np_late_fine_priority"] = data

                    data = self.work_data["np_late_fine_expiry_date"].split(',')
                    data[self.index] = self.np_late_fine_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["np_late_fine_expiry_date"] = data
                    # messagebox.showinfo(parent=self.np_late_fine_top_level,title="",message=data)
                    res = database.com_np_late_fine_entry(self.data, self.work_data)
                    if res == True:
                        self.np_late_fine_top_level.destroy()
                        self.on_close_np_late_fine_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_late_fine_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def np_late_fine_combo_fun(self, event):
        if self.np_late_fine_combo_box.get() == "NEW ENTRY":
            self.np_late_fine_amount_var.set("")
            self.np_late_fine_app_no_var.set("")
            self.np_late_fine_status_var.set("1")
            self.np_late_fine_status_change()
            self.np_late_fine_entry_selection_var = "NEW ENTRY"
            self.np_late_fine_date_lbl.config(text="")
            self.np_late_fine_time_lbl.config(text="")
            self.np_late_fine_scale.set(0)
            self.np_late_fine_expiry_date_var.set("")


        # self.data[0]["np_late_fine_amount"]
        else:
            self.np_late_fine_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.np_late_fine_combo_box.get())-1
            amount = self.work_data["np_late_fine_amount"].split(",")
            app_no = self.work_data["np_late_fine_app_no"].split(",")
            status = self.work_data["np_late_fine_status"].split(",")
            date = self.work_data["np_late_fine_date"].split(",")
            time = self.work_data["np_late_fine_time"].split(",")
            priority = self.work_data["np_late_fine_priority"].split(",")
            np_late_fine_expiry = self.work_data["np_late_fine_expiry_date"].split(",")
            self.np_late_fine_amount_var.set(amount[int(self.np_late_fine_combo_box.get())-1])
            self.np_late_fine_app_no_var.set(app_no[int(self.np_late_fine_combo_box.get())-1])
            self.np_late_fine_status_var.set(status[int(self.np_late_fine_combo_box.get())-1])
            self.np_late_fine_date_lbl.config(text=date[int(self.np_late_fine_combo_box.get())-1])
            self.np_late_fine_time_lbl.config(text=time[int(self.np_late_fine_combo_box.get())-1])
            self.np_late_fine_scale.set(self.con_value_rev(priority[int(self.np_late_fine_combo_box.get())-1]))
            self.np_late_fine_expiry_date_var.set(np_late_fine_expiry[int(self.np_late_fine_combo_box.get())-1])
            if self.np_late_fine_status_var.get() == "0":
                self.np_late_fine_status_btn.config(image=self.pending_status_img)
            elif self.np_late_fine_status_var.get() == "1":
                self.np_late_fine_status_btn.config(image=self.completed_status_img)

    def np_late_fine_entry_delete_fun(self):
        if self.np_late_fine_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["np_late_fine_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["np_late_fine_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_late_fine_amount"] = data

            data = self.work_data["np_late_fine_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_late_fine_app_no"] = data

            data = self.work_data["np_late_fine_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_late_fine_status"] = data

            data = self.work_data["np_late_fine_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_late_fine_date"] = data

            data = self.work_data["np_late_fine_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_late_fine_time"] = data

            data = self.work_data["np_late_fine_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_late_fine_priority"] = data

            data = self.work_data["np_late_fine_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_late_fine_expiry_date"] = data

            res = database.com_np_late_fine_entry(self.data, self.work_data)
            if res == True:
                self.np_late_fine_top_level.destroy()
                self.on_close_np_late_fine_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.np_late_fine_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def np_late_fine_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.np_late_fine_update_scale_color(value)  # Update scale color based on value

    def convert_np_late_fine_app_no_to_uppercase(self):
        current_text = self.np_late_fine_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.np_late_fine_app_no_var.set(uppercase_text)

















    def open_pb_permit_new_win(self):
        if not self.pb_permit_new_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.pb_permit_new_top_level_open = True
            self.pb_permit_new_top_level = Toplevel()
            self.pb_permit_new_top_level.protocol("WM_DELETE_WINDOW", self.on_close_pb_permit_new_top_level)
            self.pb_permit_new_top_level.configure(bg='#B39CD0')
            screen_width = self.pb_permit_new_top_level.winfo_screenwidth()
            screen_height = self.pb_permit_new_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.pb_permit_new_top_level.title("PB PERMIT NEW")
            self.pb_permit_new_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.pb_permit_new_top_level.winfo_screenwidth()
            screen_height = self.pb_permit_new_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.pb_permit_new_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.pb_permit_new_top_level.resizable(False, False)
            self.pb_permit_new_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\pb_permit_new_bg.png"))
            Label(master=self.pb_permit_new_top_level,
                  image=self.pb_permit_new_bg_img).pack()

            self.pb_permit_new_time_lbl = Label(self.pb_permit_new_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.pb_permit_new_time_lbl.place(x=75,y=51)

            self.pb_permit_new_date_lbl = Label(self.pb_permit_new_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.pb_permit_new_date_lbl.place(x=195, y=51)

            self.pb_permit_new_combo_box = ttk.Combobox(self.pb_permit_new_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.pb_permit_new_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.pb_permit_new_scale = ttk.Scale(self.pb_permit_new_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.pb_permit_new_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.pb_permit_new_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["pb_permit_new_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.pb_permit_new_combo_box['values'] = self.combo_values

            self.pb_permit_new_combo_box.bind('<<ComboboxSelected>>', self.pb_permit_new_combo_fun)
            self.pb_permit_new_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.pb_permit_new_amount_var = StringVar()
            self.pb_permit_new_amount_entry = Entry(self.pb_permit_new_top_level,
                                                 textvariable=self.pb_permit_new_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.pb_permit_new_amount_entry.place(x=60, y=125)

            self.pb_permit_new_app_no_var = StringVar()
            self.pb_permit_new_app_no_entry = Entry(self.pb_permit_new_top_level,
                                         textvariable=self.pb_permit_new_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.pb_permit_new_app_no_entry.place(x=60, y=196)
            self.pb_permit_new_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_pb_permit_new_app_no_to_uppercase())

            self.pb_permit_new_expiry_date_var = StringVar()
            self.pb_permit_new_expiry_date_entry = DateEntry(self.pb_permit_new_top_level,
                                                        textvariable=self.pb_permit_new_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 1,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.pb_permit_new_expiry_date_entry.place(x=325, y=200)

            self.pb_permit_new_status_var = StringVar()
            self.pb_permit_new_status_var.set("0")
            self.pb_permit_new_status_btn = Button(master=self.pb_permit_new_top_level,
                                                textvariable=self.pb_permit_new_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.pb_permit_new_status_change,
                                                borderwidth=0
                                                )
            self.pb_permit_new_status_btn.place(x=250, y=125)



            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.pb_permit_new_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_pb_permit_new_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.pb_permit_new_top_level,image=self.delete_but_img,
                   command=self.pb_permit_new_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.pb_permit_new_top_level.mainloop()

    def on_close_pb_permit_new_top_level(self):
        self.pb_permit_new_top_level_open = False
        self.pb_permit_new_top_level.destroy()
        self.windows = "closed"

    def pb_permit_new_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def pb_permit_new_status_change(self):
        if self.pb_permit_new_status_var.get() == "0":
            self.pb_permit_new_status_btn.config(image=self.completed_status_img)
            self.pb_permit_new_status_var.set("1")
            print(self.pb_permit_new_status_var.get())
        elif self.pb_permit_new_status_var.get() == "1":
            self.pb_permit_new_status_btn.config(image=self.pending_status_img)
            self.pb_permit_new_status_var.set("0")
            print(self.pb_permit_new_status_var.get())

    def com_pb_permit_new_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.pb_permit_new_priority_var.get()))
        if self.pb_permit_new_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.pb_permit_new_top_level)
        elif self.pb_permit_new_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.pb_permit_new_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("pb_permit_new_amount") == None:
                print("1")
                if self.pb_permit_new_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["pb_permit_new_amount"] = self.pb_permit_new_amount_var.get()+","
                    self.data1["pb_permit_new_app_no"] = self.pb_permit_new_app_no_var.get()+","
                    self.data1["pb_permit_new_status"] = self.pb_permit_new_status_var.get()+","
                    self.data1["pb_permit_new_time"] = formatted_time + ","
                    self.data1["pb_permit_new_date"] = formatted_date + ","
                    self.data1["pb_permit_new_priority"] = self.con_value(round(self.pb_permit_new_scale.get()))+","
                    self.data1["pb_permit_new_expiry_date"] = self.pb_permit_new_expiry_date_var.get()+","





                    # adding pb_permit_new amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_permit_new_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_pb_permit_new_entry(self.data, self.data1)
                    if res == True:
                        self.pb_permit_new_top_level.destroy()
                        self.on_close_pb_permit_new_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_permit_new_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("pb_permit_new_amount") != None:
                print("2.0")
                if self.pb_permit_new_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["pb_permit_new_amount"] = self.work_data["pb_permit_new_amount"] +self.pb_permit_new_amount_var.get()+","
                    self.data1["pb_permit_new_app_no"] = self.work_data["pb_permit_new_app_no"] +self.pb_permit_new_app_no_var.get()+","
                    self.data1["pb_permit_new_status"] = self.work_data["pb_permit_new_status"] +self.pb_permit_new_status_var.get()+","
                    self.data1["pb_permit_new_time"] = self.work_data["pb_permit_new_time"] + formatted_time + ","
                    self.data1["pb_permit_new_date"] = self.work_data["pb_permit_new_date"] +formatted_date + ","
                    self.data1["pb_permit_new_priority"] = self.work_data["pb_permit_new_priority"] +self.con_value(round(self.pb_permit_new_scale.get()))+","
                    self.data1["pb_permit_new_expiry_date"] = self.work_data["pb_permit_new_expiry_date"] +self.pb_permit_new_expiry_date_var.get()+","





                    # adding pb_permit_new amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_permit_new_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_pb_permit_new_entry(self.data, self.data1)
                    if res == True:
                        self.pb_permit_new_top_level.destroy()
                        self.on_close_pb_permit_new_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_permit_new_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.pb_permit_new_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["pb_permit_new_amount"].split(',')
                    # removing old amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of redispatch
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_permit_new_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    data = self.work_data["pb_permit_new_amount"].split(',')
                    data[self.index] = self.pb_permit_new_amount_entry.get()
                    data =",".join(data)
                    self.work_data["pb_permit_new_amount"] = data

                    data = self.work_data["pb_permit_new_app_no"].split(',')
                    data[self.index] = self.pb_permit_new_app_no_var.get()
                    data =",".join(data)
                    self.work_data["pb_permit_new_app_no"] = data

                    data = self.work_data["pb_permit_new_status"].split(',')
                    data[self.index] = self.pb_permit_new_status_var.get()
                    data =",".join(data)
                    self.work_data["pb_permit_new_status"] = data

                    data = self.work_data["pb_permit_new_priority"].split(',')
                    data[self.index] = self.con_value(round(self.pb_permit_new_scale.get()))
                    data =",".join(data)
                    self.work_data["pb_permit_new_priority"] = data

                    data = self.work_data["pb_permit_new_expiry_date"].split(',')
                    data[self.index] = self.pb_permit_new_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["pb_permit_new_expiry_date"] = data
                    # messagebox.showinfo(parent=self.pb_permit_new_top_level,title="",message=data)
                    res = database.com_pb_permit_new_entry(self.data, self.work_data)
                    if res == True:
                        self.pb_permit_new_top_level.destroy()
                        self.on_close_pb_permit_new_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_permit_new_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def pb_permit_new_combo_fun(self, event):
        if self.pb_permit_new_combo_box.get() == "NEW ENTRY":
            self.pb_permit_new_amount_var.set("")
            self.pb_permit_new_app_no_var.set("")
            self.pb_permit_new_status_var.set("1")
            self.pb_permit_new_status_change()
            self.pb_permit_new_entry_selection_var = "NEW ENTRY"
            self.pb_permit_new_date_lbl.config(text="")
            self.pb_permit_new_time_lbl.config(text="")
            self.pb_permit_new_scale.set(0)
            self.pb_permit_new_expiry_date_var.set("")


        # self.data[0]["pb_permit_new_amount"]
        else:
            self.pb_permit_new_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.pb_permit_new_combo_box.get())-1
            amount = self.work_data["pb_permit_new_amount"].split(",")
            app_no = self.work_data["pb_permit_new_app_no"].split(",")
            status = self.work_data["pb_permit_new_status"].split(",")
            date = self.work_data["pb_permit_new_date"].split(",")
            time = self.work_data["pb_permit_new_time"].split(",")
            priority = self.work_data["pb_permit_new_priority"].split(",")
            pb_permit_new_expiry = self.work_data["pb_permit_new_expiry_date"].split(",")
            self.pb_permit_new_amount_var.set(amount[int(self.pb_permit_new_combo_box.get())-1])
            self.pb_permit_new_app_no_var.set(app_no[int(self.pb_permit_new_combo_box.get())-1])
            self.pb_permit_new_status_var.set(status[int(self.pb_permit_new_combo_box.get())-1])
            self.pb_permit_new_date_lbl.config(text=date[int(self.pb_permit_new_combo_box.get())-1])
            self.pb_permit_new_time_lbl.config(text=time[int(self.pb_permit_new_combo_box.get())-1])
            self.pb_permit_new_scale.set(self.con_value_rev(priority[int(self.pb_permit_new_combo_box.get())-1]))
            self.pb_permit_new_expiry_date_var.set(pb_permit_new_expiry[int(self.pb_permit_new_combo_box.get())-1])
            if self.pb_permit_new_status_var.get() == "0":
                self.pb_permit_new_status_btn.config(image=self.pending_status_img)
            elif self.pb_permit_new_status_var.get() == "1":
                self.pb_permit_new_status_btn.config(image=self.completed_status_img)

    def pb_permit_new_entry_delete_fun(self):
        if self.pb_permit_new_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["pb_permit_new_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["pb_permit_new_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_permit_new_amount"] = data

            data = self.work_data["pb_permit_new_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_permit_new_app_no"] = data

            data = self.work_data["pb_permit_new_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_permit_new_status"] = data

            data = self.work_data["pb_permit_new_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_permit_new_date"] = data

            data = self.work_data["pb_permit_new_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_permit_new_time"] = data

            data = self.work_data["pb_permit_new_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_permit_new_priority"] = data

            data = self.work_data["pb_permit_new_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_permit_new_expiry_date"] = data

            res = database.com_pb_permit_new_entry(self.data, self.work_data)
            if res == True:
                self.pb_permit_new_top_level.destroy()
                self.on_close_pb_permit_new_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.pb_permit_new_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def pb_permit_new_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.pb_permit_new_update_scale_color(value)  # Update scale color based on value

    def convert_pb_permit_new_app_no_to_uppercase(self):
        current_text = self.pb_permit_new_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.pb_permit_new_app_no_var.set(uppercase_text)



















    def open_np_permit_win(self):
        if not self.np_permit_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.np_permit_top_level_open = True
            self.np_permit_top_level = Toplevel()
            self.np_permit_top_level.protocol("WM_DELETE_WINDOW", self.on_close_np_permit_top_level)
            self.np_permit_top_level.configure(bg='#B39CD0')
            screen_width = self.np_permit_top_level.winfo_screenwidth()
            screen_height = self.np_permit_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.np_permit_top_level.title("NP PERMIT")
            self.np_permit_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.np_permit_top_level.winfo_screenwidth()
            screen_height = self.np_permit_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.np_permit_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.np_permit_top_level.resizable(False, False)
            self.np_permit_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\np_permit_bg.png"))
            Label(master=self.np_permit_top_level,
                  image=self.np_permit_bg_img).pack()

            self.np_permit_time_lbl = Label(self.np_permit_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.np_permit_time_lbl.place(x=75,y=51)

            self.np_permit_date_lbl = Label(self.np_permit_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.np_permit_date_lbl.place(x=195, y=51)

            self.np_permit_combo_box = ttk.Combobox(self.np_permit_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.np_permit_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.np_permit_scale = ttk.Scale(self.np_permit_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.np_permit_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.np_permit_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["np_permit_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.np_permit_combo_box['values'] = self.combo_values

            self.np_permit_combo_box.bind('<<ComboboxSelected>>', self.np_permit_combo_fun)
            self.np_permit_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.np_permit_amount_var = StringVar()
            self.np_permit_amount_entry = Entry(self.np_permit_top_level,
                                                 textvariable=self.np_permit_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.np_permit_amount_entry.place(x=60, y=125)

            self.np_permit_app_no_var = StringVar()
            self.np_permit_app_no_entry = Entry(self.np_permit_top_level,
                                         textvariable=self.np_permit_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.np_permit_app_no_entry.place(x=60, y=196)
            self.np_permit_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_np_permit_app_no_to_uppercase())

            self.np_permit_expiry_date_var = StringVar()
            self.np_permit_expiry_date_entry = DateEntry(self.np_permit_top_level,
                                                        textvariable=self.np_permit_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 1,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.np_permit_expiry_date_entry.place(x=325, y=200)

            self.np_permit_status_var = StringVar()
            self.np_permit_status_var.set("0")
            self.np_permit_status_btn = Button(master=self.np_permit_top_level,
                                                textvariable=self.np_permit_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.np_permit_status_change,
                                                borderwidth=0
                                                )
            self.np_permit_status_btn.place(x=250, y=125)



            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.np_permit_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_np_permit_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.np_permit_top_level,image=self.delete_but_img,
                   command=self.np_permit_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.np_permit_top_level.mainloop()

    def on_close_np_permit_top_level(self):
        self.np_permit_top_level_open = False
        self.np_permit_top_level.destroy()
        self.windows = "closed"

    def np_permit_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def np_permit_status_change(self):
        if self.np_permit_status_var.get() == "0":
            self.np_permit_status_btn.config(image=self.completed_status_img)
            self.np_permit_status_var.set("1")
            print(self.np_permit_status_var.get())
        elif self.np_permit_status_var.get() == "1":
            self.np_permit_status_btn.config(image=self.pending_status_img)
            self.np_permit_status_var.set("0")
            print(self.np_permit_status_var.get())

    def com_np_permit_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.np_permit_priority_var.get()))
        if self.np_permit_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.np_permit_top_level)
        elif self.np_permit_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.np_permit_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("np_permit_amount") == None:
                print("1")
                if self.np_permit_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["np_permit_amount"] = self.np_permit_amount_var.get()+","
                    self.data1["np_permit_app_no"] = self.np_permit_app_no_var.get()+","
                    self.data1["np_permit_status"] = self.np_permit_status_var.get()+","
                    self.data1["np_permit_time"] = formatted_time + ","
                    self.data1["np_permit_date"] = formatted_date + ","
                    self.data1["np_permit_priority"] = self.con_value(round(self.np_permit_scale.get()))+","
                    self.data1["np_permit_expiry_date"] = self.np_permit_expiry_date_var.get()+","





                    # adding np_permit amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_permit_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_np_permit_entry(self.data, self.data1)
                    if res == True:
                        self.np_permit_top_level.destroy()
                        self.on_close_np_permit_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_permit_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("np_permit_amount") != None:
                print("2.0")
                if self.np_permit_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["np_permit_amount"] = self.work_data["np_permit_amount"] +self.np_permit_amount_var.get()+","
                    self.data1["np_permit_app_no"] = self.work_data["np_permit_app_no"] +self.np_permit_app_no_var.get()+","
                    self.data1["np_permit_status"] = self.work_data["np_permit_status"] +self.np_permit_status_var.get()+","
                    self.data1["np_permit_time"] = self.work_data["np_permit_time"] + formatted_time + ","
                    self.data1["np_permit_date"] = self.work_data["np_permit_date"] +formatted_date + ","
                    self.data1["np_permit_priority"] = self.work_data["np_permit_priority"] +self.con_value(round(self.np_permit_scale.get()))+","
                    self.data1["np_permit_expiry_date"] = self.work_data["np_permit_expiry_date"] +self.np_permit_expiry_date_var.get()+","





                    # adding np_permit amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_permit_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    res = database.com_np_permit_entry(self.data, self.data1)
                    if res == True:
                        self.np_permit_top_level.destroy()
                        self.on_close_np_permit_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_permit_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.np_permit_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["np_permit_amount"].split(',')
                    # removing old amount of np_permit
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of np_permit
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_permit_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["np_permit_amount"].split(',')
                    data[self.index] = self.np_permit_amount_entry.get()
                    data =",".join(data)
                    self.work_data["np_permit_amount"] = data

                    data = self.work_data["np_permit_app_no"].split(',')
                    data[self.index] = self.np_permit_app_no_var.get()
                    data =",".join(data)
                    self.work_data["np_permit_app_no"] = data

                    data = self.work_data["np_permit_status"].split(',')
                    data[self.index] = self.np_permit_status_var.get()
                    data =",".join(data)
                    self.work_data["np_permit_status"] = data

                    data = self.work_data["np_permit_priority"].split(',')
                    data[self.index] = self.con_value(round(self.np_permit_scale.get()))
                    data =",".join(data)
                    self.work_data["np_permit_priority"] = data

                    data = self.work_data["np_permit_expiry_date"].split(',')
                    data[self.index] = self.np_permit_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["np_permit_expiry_date"] = data
                    # messagebox.showinfo(parent=self.np_permit_top_level,title="",message=data)
                    res = database.com_np_permit_entry(self.data, self.work_data)
                    if res == True:
                        self.np_permit_top_level.destroy()
                        self.on_close_np_permit_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_permit_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def np_permit_combo_fun(self, event):
        if self.np_permit_combo_box.get() == "NEW ENTRY":
            self.np_permit_amount_var.set("")
            self.np_permit_app_no_var.set("")
            self.np_permit_status_var.set("1")
            self.np_permit_status_change()
            self.np_permit_entry_selection_var = "NEW ENTRY"
            self.np_permit_date_lbl.config(text="")
            self.np_permit_time_lbl.config(text="")
            self.np_permit_scale.set(0)
            self.np_permit_expiry_date_var.set("")


        # self.data[0]["np_permit_amount"]
        else:
            self.np_permit_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.np_permit_combo_box.get())-1
            amount = self.work_data["np_permit_amount"].split(",")
            app_no = self.work_data["np_permit_app_no"].split(",")
            status = self.work_data["np_permit_status"].split(",")
            date = self.work_data["np_permit_date"].split(",")
            time = self.work_data["np_permit_time"].split(",")
            priority = self.work_data["np_permit_priority"].split(",")
            np_permit_expiry = self.work_data["np_permit_expiry_date"].split(",")
            self.np_permit_amount_var.set(amount[int(self.np_permit_combo_box.get())-1])
            self.np_permit_app_no_var.set(app_no[int(self.np_permit_combo_box.get())-1])
            self.np_permit_status_var.set(status[int(self.np_permit_combo_box.get())-1])
            self.np_permit_date_lbl.config(text=date[int(self.np_permit_combo_box.get())-1])
            self.np_permit_time_lbl.config(text=time[int(self.np_permit_combo_box.get())-1])
            self.np_permit_scale.set(self.con_value_rev(priority[int(self.np_permit_combo_box.get())-1]))
            self.np_permit_expiry_date_var.set(np_permit_expiry[int(self.np_permit_combo_box.get())-1])
            if self.np_permit_status_var.get() == "0":
                self.np_permit_status_btn.config(image=self.pending_status_img)
            elif self.np_permit_status_var.get() == "1":
                self.np_permit_status_btn.config(image=self.completed_status_img)

    def np_permit_entry_delete_fun(self):
        if self.np_permit_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["np_permit_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["np_permit_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_permit_amount"] = data

            data = self.work_data["np_permit_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_permit_app_no"] = data

            data = self.work_data["np_permit_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_permit_status"] = data

            data = self.work_data["np_permit_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_permit_date"] = data

            data = self.work_data["np_permit_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_permit_time"] = data

            data = self.work_data["np_permit_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_permit_priority"] = data

            data = self.work_data["np_permit_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_permit_expiry_date"] = data

            res = database.com_np_permit_entry(self.data, self.work_data)
            if res == True:
                self.np_permit_top_level.destroy()
                self.on_close_np_permit_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.np_permit_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def np_permit_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.np_permit_update_scale_color(value)  # Update scale color based on value

    def convert_np_permit_app_no_to_uppercase(self):
        current_text = self.np_permit_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.np_permit_app_no_var.set(uppercase_text)




















    def open_alteration_win(self):
        if not self.alteration_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.alteration_top_level_open = True
            self.alteration_top_level = Toplevel()
            self.alteration_top_level.protocol("WM_DELETE_WINDOW", self.on_close_alteration_top_level)
            self.alteration_top_level.configure(bg='#B39CD0')
            screen_width = self.alteration_top_level.winfo_screenwidth()
            screen_height = self.alteration_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.alteration_top_level.title("ALTERATION")
            self.alteration_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.alteration_top_level.winfo_screenwidth()
            screen_height = self.alteration_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.alteration_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.alteration_top_level.resizable(False, False)
            self.alteration_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\alteration_bg.png"))
            Label(master=self.alteration_top_level,
                  image=self.alteration_bg_img).pack()

            self.alteration_time_lbl = Label(self.alteration_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.alteration_time_lbl.place(x=75,y=51)

            self.alteration_date_lbl = Label(self.alteration_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.alteration_date_lbl.place(x=195, y=51)

            self.alteration_combo_box = ttk.Combobox(self.alteration_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.alteration_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.alteration_scale = ttk.Scale(self.alteration_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.alteration_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.alteration_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["alteration_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.alteration_combo_box['values'] = self.combo_values

            self.alteration_combo_box.bind('<<ComboboxSelected>>', self.alteration_combo_fun)
            self.alteration_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.alteration_amount_var = StringVar()
            self.alteration_amount_entry = Entry(self.alteration_top_level,
                                                 textvariable=self.alteration_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.alteration_amount_entry.place(x=60, y=125)

            self.alteration_app_no_var = StringVar()
            self.alteration_app_no_entry = Entry(self.alteration_top_level,
                                         textvariable=self.alteration_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.alteration_app_no_entry.place(x=60, y=196)
            self.alteration_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_alteration_app_no_to_uppercase())

            self.alteration_status_var = StringVar()
            self.alteration_status_var.set("0")
            self.alteration_status_btn = Button(master=self.alteration_top_level,
                                                textvariable=self.alteration_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.alteration_status_change,
                                                borderwidth=0
                                                )
            self.alteration_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.alteration_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_alteration_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.alteration_top_level,image=self.delete_but_img,
                   command=self.alteration_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.alteration_top_level.mainloop()

    def on_close_alteration_top_level(self):
        self.alteration_top_level_open = False
        self.alteration_top_level.destroy()
        self.windows = "closed"

    def alteration_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def alteration_status_change(self):
        if self.alteration_status_var.get() == "0":
            self.alteration_status_btn.config(image=self.completed_status_img)
            self.alteration_status_var.set("1")
            print(self.alteration_status_var.get())
        elif self.alteration_status_var.get() == "1":
            self.alteration_status_btn.config(image=self.pending_status_img)
            self.alteration_status_var.set("0")
            print(self.alteration_status_var.get())

    def com_alteration_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.alteration_priority_var.get()))
        if self.alteration_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.alteration_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("alteration_amount") == None:
                print("1")
                if self.alteration_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["alteration_amount"] = self.alteration_amount_var.get()+","
                    self.data1["alteration_app_no"] = self.alteration_app_no_var.get()+","
                    self.data1["alteration_status"] = self.alteration_status_var.get()+","
                    self.data1["alteration_time"] = formatted_time + ","
                    self.data1["alteration_date"] = formatted_date + ","
                    self.data1["alteration_priority"] = self.con_value(round(self.alteration_scale.get()))+","





                    # adding alteration amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.alteration_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_alteration_entry(self.data, self.data1)
                    if res == True:
                        self.alteration_top_level.destroy()
                        self.on_close_alteration_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.alteration_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("alteration_amount") != None:
                print("2.0")
                if self.alteration_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["alteration_amount"] = self.work_data["alteration_amount"] +self.alteration_amount_var.get()+","
                    self.data1["alteration_app_no"] = self.work_data["alteration_app_no"] +self.alteration_app_no_var.get()+","
                    self.data1["alteration_status"] = self.work_data["alteration_status"] +self.alteration_status_var.get()+","
                    self.data1["alteration_time"] = self.work_data["alteration_time"] + formatted_time + ","
                    self.data1["alteration_date"] = self.work_data["alteration_date"] +formatted_date + ","
                    self.data1["alteration_priority"] = self.work_data["alteration_priority"] +self.con_value(round(self.alteration_scale.get()))+","




                    # adding alteration amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.alteration_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]




                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])
                    res = database.com_alteration_entry(self.data, self.data1)
                    if res == True:
                        self.alteration_top_level.destroy()
                        self.on_close_alteration_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.alteration_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.alteration_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["alteration_amount"].split(',')
                    # removing old amount of alteration
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of alteration
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.alteration_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["alteration_amount"].split(',')
                    data[self.index] = self.alteration_amount_entry.get()
                    data =",".join(data)
                    self.work_data["alteration_amount"] = data

                    data = self.work_data["alteration_app_no"].split(',')
                    data[self.index] = self.alteration_app_no_var.get()
                    data =",".join(data)
                    self.work_data["alteration_app_no"] = data

                    data = self.work_data["alteration_status"].split(',')
                    data[self.index] = self.alteration_status_var.get()
                    data =",".join(data)
                    self.work_data["alteration_status"] = data

                    data = self.work_data["alteration_priority"].split(',')
                    data[self.index] = self.con_value(round(self.alteration_scale.get()))
                    data =",".join(data)
                    self.work_data["alteration_priority"] = data
                    # messagebox.showinfo(parent=self.alteration_top_level,title="",message=data)
                    res = database.com_alteration_entry(self.data, self.work_data)
                    if res == True:
                        self.alteration_top_level.destroy()
                        self.on_close_alteration_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.alteration_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def alteration_combo_fun(self, event):
        if self.alteration_combo_box.get() == "NEW ENTRY":
            self.alteration_amount_var.set("")
            self.alteration_app_no_var.set("")
            self.alteration_status_var.set("1")
            self.alteration_status_change()
            self.alteration_entry_selection_var = "NEW ENTRY"
            self.alteration_date_lbl.config(text="")
            self.alteration_time_lbl.config(text="")
            self.alteration_scale.set(0)


        # self.data[0]["alteration_amount"]
        else:
            self.alteration_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.alteration_combo_box.get())-1
            amount = self.work_data["alteration_amount"].split(",")
            app_no = self.work_data["alteration_app_no"].split(",")
            status = self.work_data["alteration_status"].split(",")
            date = self.work_data["alteration_date"].split(",")
            time = self.work_data["alteration_time"].split(",")
            priority = self.work_data["alteration_priority"].split(",")
            self.alteration_amount_var.set(amount[int(self.alteration_combo_box.get())-1])
            self.alteration_app_no_var.set(app_no[int(self.alteration_combo_box.get())-1])
            self.alteration_status_var.set(status[int(self.alteration_combo_box.get())-1])
            self.alteration_date_lbl.config(text=date[int(self.alteration_combo_box.get())-1])
            self.alteration_time_lbl.config(text=time[int(self.alteration_combo_box.get())-1])
            self.alteration_scale.set(self.con_value_rev(priority[int(self.alteration_combo_box.get())-1]))
            if self.alteration_status_var.get() == "0":
                self.alteration_status_btn.config(image=self.pending_status_img)
            elif self.alteration_status_var.get() == "1":
                self.alteration_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.alteration_top_level, title="",message="")

    def alteration_entry_delete_fun(self):
        if self.alteration_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["alteration_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["alteration_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["alteration_amount"] = data

            data = self.work_data["alteration_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["alteration_app_no"] = data

            data = self.work_data["alteration_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["alteration_status"] = data

            data = self.work_data["alteration_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["alteration_date"] = data

            data = self.work_data["alteration_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["alteration_time"] = data

            data = self.work_data["alteration_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["alteration_priority"] = data

            res = database.com_alteration_entry(self.data, self.work_data)
            if res == True:
                self.alteration_top_level.destroy()
                self.on_close_alteration_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.alteration_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def alteration_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.alteration_update_scale_color(value)  # Update scale color based on value

    def convert_alteration_app_no_to_uppercase(self):
        current_text = self.alteration_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.alteration_app_no_var.set(uppercase_text)



















    def open_tax_win(self):
        if not self.tax_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.tax_top_level_open = True
            self.tax_top_level = Toplevel()
            self.tax_top_level.protocol("WM_DELETE_WINDOW", self.on_close_tax_top_level)
            self.tax_top_level.configure(bg='#B39CD0')
            screen_width = self.tax_top_level.winfo_screenwidth()
            screen_height = self.tax_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.tax_top_level.title("TAX")
            self.tax_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.tax_top_level.winfo_screenwidth()
            screen_height = self.tax_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.tax_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.tax_top_level.resizable(False, False)
            self.tax_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\tax_bg.png"))
            Label(master=self.tax_top_level,
                  image=self.tax_bg_img).pack()

            self.tax_time_lbl = Label(self.tax_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.tax_time_lbl.place(x=75,y=51)

            self.tax_date_lbl = Label(self.tax_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.tax_date_lbl.place(x=195, y=51)

            self.tax_combo_box = ttk.Combobox(self.tax_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.tax_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.tax_scale = ttk.Scale(self.tax_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.tax_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.tax_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["tax_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.tax_combo_box['values'] = self.combo_values

            self.tax_combo_box.bind('<<ComboboxSelected>>', self.tax_combo_fun)
            self.tax_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.tax_amount_var = StringVar()
            self.tax_amount_entry = Entry(self.tax_top_level,
                                                 textvariable=self.tax_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.tax_amount_entry.place(x=60, y=125)

            self.tax_app_no_var = StringVar()
            self.tax_app_no_entry = Entry(self.tax_top_level,
                                         textvariable=self.tax_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.tax_app_no_entry.place(x=60, y=196)
            self.tax_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_tax_app_no_to_uppercase())

            self.tax_expiry_date_var = StringVar()
            self.tax_expiry_date_entry = DateEntry(self.tax_top_level,
                                                        textvariable=self.tax_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 1,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.tax_expiry_date_entry.place(x=325, y=200)

            self.tax_status_var = StringVar()
            self.tax_status_var.set("0")
            self.tax_status_btn = Button(master=self.tax_top_level,
                                                textvariable=self.tax_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.tax_status_change,
                                                borderwidth=0
                                                )
            self.tax_status_btn.place(x=250, y=125)



            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.tax_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_tax_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.tax_top_level,image=self.delete_but_img,
                   command=self.tax_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.tax_top_level.mainloop()

    def on_close_tax_top_level(self):
        self.tax_top_level_open = False
        self.tax_top_level.destroy()
        self.windows = "closed"

    def tax_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def tax_status_change(self):
        if self.tax_status_var.get() == "0":
            self.tax_status_btn.config(image=self.completed_status_img)
            self.tax_status_var.set("1")
            print(self.tax_status_var.get())
        elif self.tax_status_var.get() == "1":
            self.tax_status_btn.config(image=self.pending_status_img)
            self.tax_status_var.set("0")
            print(self.tax_status_var.get())

    def com_tax_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.tax_priority_var.get()))
        if self.tax_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.tax_top_level)
        elif self.tax_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.tax_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("tax_amount") == None:
                print("1")
                if self.tax_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["tax_amount"] = self.tax_amount_var.get()+","
                    self.data1["tax_app_no"] = self.tax_app_no_var.get()+","
                    self.data1["tax_status"] = self.tax_status_var.get()+","
                    self.data1["tax_time"] = formatted_time + ","
                    self.data1["tax_date"] = formatted_date + ","
                    self.data1["tax_priority"] = self.con_value(round(self.tax_scale.get()))+","
                    self.data1["tax_expiry_date"] = self.tax_expiry_date_var.get()+","




                    # adding tax amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.tax_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_tax_entry(self.data, self.data1)
                    if res == True:
                        self.tax_top_level.destroy()
                        self.on_close_tax_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.tax_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("tax_amount") != None:
                print("2.0")
                if self.tax_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["tax_amount"] = self.work_data["tax_amount"] +self.tax_amount_var.get()+","
                    self.data1["tax_app_no"] = self.work_data["tax_app_no"] +self.tax_app_no_var.get()+","
                    self.data1["tax_status"] = self.work_data["tax_status"] +self.tax_status_var.get()+","
                    self.data1["tax_time"] = self.work_data["tax_time"] + formatted_time + ","
                    self.data1["tax_date"] = self.work_data["tax_date"] +formatted_date + ","
                    self.data1["tax_priority"] = self.work_data["tax_priority"] +self.con_value(round(self.tax_scale.get()))+","
                    self.data1["tax_expiry_date"] = self.work_data["tax_expiry_date"] +self.tax_expiry_date_var.get()+","




                    # adding tax amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.tax_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_tax_entry(self.data, self.data1)
                    if res == True:
                        self.tax_top_level.destroy()
                        self.on_close_tax_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.tax_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.tax_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["tax_amount"].split(',')
                    # removing old amount of tax
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of tax
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.tax_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    data = self.work_data["tax_amount"].split(',')
                    data[self.index] = self.tax_amount_entry.get()
                    data =",".join(data)
                    self.work_data["tax_amount"] = data

                    data = self.work_data["tax_app_no"].split(',')
                    data[self.index] = self.tax_app_no_var.get()
                    data =",".join(data)
                    self.work_data["tax_app_no"] = data

                    data = self.work_data["tax_status"].split(',')
                    data[self.index] = self.tax_status_var.get()
                    data =",".join(data)
                    self.work_data["tax_status"] = data

                    data = self.work_data["tax_priority"].split(',')
                    data[self.index] = self.con_value(round(self.tax_scale.get()))
                    data =",".join(data)
                    self.work_data["tax_priority"] = data

                    data = self.work_data["tax_expiry_date"].split(',')
                    data[self.index] = self.tax_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["tax_expiry_date"] = data
                    # messagebox.showinfo(parent=self.tax_top_level,title="",message=data)
                    res = database.com_tax_entry(self.data, self.work_data)
                    if res == True:
                        self.tax_top_level.destroy()
                        self.on_close_tax_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.tax_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def tax_combo_fun(self, event):
        if self.tax_combo_box.get() == "NEW ENTRY":
            self.tax_amount_var.set("")
            self.tax_app_no_var.set("")
            self.tax_status_var.set("1")
            self.tax_status_change()
            self.tax_entry_selection_var = "NEW ENTRY"
            self.tax_date_lbl.config(text="")
            self.tax_time_lbl.config(text="")
            self.tax_scale.set(0)
            self.tax_expiry_date_var.set("")


        # self.data[0]["tax_amount"]
        else:
            self.tax_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.tax_combo_box.get())-1
            amount = self.work_data["tax_amount"].split(",")
            app_no = self.work_data["tax_app_no"].split(",")
            status = self.work_data["tax_status"].split(",")
            date = self.work_data["tax_date"].split(",")
            time = self.work_data["tax_time"].split(",")
            priority = self.work_data["tax_priority"].split(",")
            tax_expiry = self.work_data["tax_expiry_date"].split(",")
            self.tax_amount_var.set(amount[int(self.tax_combo_box.get())-1])
            self.tax_app_no_var.set(app_no[int(self.tax_combo_box.get())-1])
            self.tax_status_var.set(status[int(self.tax_combo_box.get())-1])
            self.tax_date_lbl.config(text=date[int(self.tax_combo_box.get())-1])
            self.tax_time_lbl.config(text=time[int(self.tax_combo_box.get())-1])
            self.tax_scale.set(self.con_value_rev(priority[int(self.tax_combo_box.get())-1]))
            self.tax_expiry_date_var.set(tax_expiry[int(self.tax_combo_box.get())-1])
            if self.tax_status_var.get() == "0":
                self.tax_status_btn.config(image=self.pending_status_img)
            elif self.tax_status_var.get() == "1":
                self.tax_status_btn.config(image=self.completed_status_img)

    def tax_entry_delete_fun(self):
        if self.tax_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)





            # these three line of code, subtract delete work amount from total
            data = self.work_data["tax_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["tax_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_amount"] = data

            data = self.work_data["tax_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_app_no"] = data

            data = self.work_data["tax_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_status"] = data

            data = self.work_data["tax_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_date"] = data

            data = self.work_data["tax_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_time"] = data

            data = self.work_data["tax_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_priority"] = data

            data = self.work_data["tax_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_expiry_date"] = data

            res = database.com_tax_entry(self.data, self.work_data)
            if res == True:
                self.tax_top_level.destroy()
                self.on_close_tax_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.tax_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def tax_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.tax_update_scale_color(value)  # Update scale color based on value

    def convert_tax_app_no_to_uppercase(self):
        current_text = self.tax_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.tax_app_no_var.set(uppercase_text)



















    def open_tax_no_due_win(self):
        if not self.tax_no_due_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.tax_no_due_top_level_open = True
            self.tax_no_due_top_level = Toplevel()
            self.tax_no_due_top_level.protocol("WM_DELETE_WINDOW", self.on_close_tax_no_due_top_level)
            self.tax_no_due_top_level.configure(bg='#B39CD0')
            screen_width = self.tax_no_due_top_level.winfo_screenwidth()
            screen_height = self.tax_no_due_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.tax_no_due_top_level.title("TAX NO DUE")
            self.tax_no_due_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.tax_no_due_top_level.winfo_screenwidth()
            screen_height = self.tax_no_due_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.tax_no_due_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.tax_no_due_top_level.resizable(False, False)
            self.tax_no_due_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\tax_no_due_bg.png"))
            Label(master=self.tax_no_due_top_level,
                  image=self.tax_no_due_bg_img).pack()

            self.tax_no_due_time_lbl = Label(self.tax_no_due_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.tax_no_due_time_lbl.place(x=75,y=51)

            self.tax_no_due_date_lbl = Label(self.tax_no_due_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.tax_no_due_date_lbl.place(x=195, y=51)

            self.tax_no_due_combo_box = ttk.Combobox(self.tax_no_due_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.tax_no_due_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.tax_no_due_scale = ttk.Scale(self.tax_no_due_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.tax_no_due_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.tax_no_due_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["tax_no_due_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.tax_no_due_combo_box['values'] = self.combo_values

            self.tax_no_due_combo_box.bind('<<ComboboxSelected>>', self.tax_no_due_combo_fun)
            self.tax_no_due_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.tax_no_due_amount_var = StringVar()
            self.tax_no_due_amount_entry = Entry(self.tax_no_due_top_level,
                                                 textvariable=self.tax_no_due_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.tax_no_due_amount_entry.place(x=60, y=125)

            self.tax_no_due_app_no_var = StringVar()
            self.tax_no_due_app_no_entry = Entry(self.tax_no_due_top_level,
                                         textvariable=self.tax_no_due_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.tax_no_due_app_no_entry.place(x=60, y=196)
            self.tax_no_due_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_tax_no_due_app_no_to_uppercase())

            self.tax_no_due_expiry_date_var = StringVar()
            self.tax_no_due_expiry_date_entry = DateEntry(self.tax_no_due_top_level,
                                                        textvariable=self.tax_no_due_expiry_date_var,
                                                        date_pattern='dd-MM-yyyy',
                                                        # state="disabled",
                                                        bg="pink", border=0,
                                                        width=self.field_width2 + 1,
                                                        font=("Helvetica", self.date_entry_size)
                                                       )
            self.tax_no_due_expiry_date_entry.place(x=325, y=200)

            self.tax_no_due_status_var = StringVar()
            self.tax_no_due_status_var.set("0")
            self.tax_no_due_status_btn = Button(master=self.tax_no_due_top_level,
                                                textvariable=self.tax_no_due_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.tax_no_due_status_change,
                                                borderwidth=0
                                                )
            self.tax_no_due_status_btn.place(x=250, y=125)



            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.tax_no_due_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_tax_no_due_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.tax_no_due_top_level,image=self.delete_but_img,
                   command=self.tax_no_due_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.tax_no_due_top_level.mainloop()

    def on_close_tax_no_due_top_level(self):
        self.tax_no_due_top_level_open = False
        self.tax_no_due_top_level.destroy()
        self.windows = "closed"

    def tax_no_due_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def tax_no_due_status_change(self):
        if self.tax_no_due_status_var.get() == "0":
            self.tax_no_due_status_btn.config(image=self.completed_status_img)
            self.tax_no_due_status_var.set("1")
            print(self.tax_no_due_status_var.get())
        elif self.tax_no_due_status_var.get() == "1":
            self.tax_no_due_status_btn.config(image=self.pending_status_img)
            self.tax_no_due_status_var.set("0")
            print(self.tax_no_due_status_var.get())

    def com_tax_no_due_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.tax_no_due_priority_var.get()))
        if self.tax_no_due_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.tax_no_due_top_level)
        elif self.tax_no_due_expiry_date_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Select Expiry Date",parent=self.tax_no_due_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("tax_no_due_amount") == None:
                print("1")
                if self.tax_no_due_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["tax_no_due_amount"] = self.tax_no_due_amount_var.get()+","
                    self.data1["tax_no_due_app_no"] = self.tax_no_due_app_no_var.get()+","
                    self.data1["tax_no_due_status"] = self.tax_no_due_status_var.get()+","
                    self.data1["tax_no_due_time"] = formatted_time + ","
                    self.data1["tax_no_due_date"] = formatted_date + ","
                    self.data1["tax_no_due_priority"] = self.con_value(round(self.tax_no_due_scale.get()))+","
                    self.data1["tax_no_due_expiry_date"] = self.tax_no_due_expiry_date_var.get()+","




                    # adding tax_no_due amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.tax_no_due_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_tax_no_due_entry(self.data, self.data1)
                    if res == True:
                        self.tax_no_due_top_level.destroy()
                        self.on_close_tax_no_due_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.tax_no_due_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("tax_no_due_amount") != None:
                print("2.0")
                if self.tax_no_due_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["tax_no_due_amount"] = self.work_data["tax_no_due_amount"] +self.tax_no_due_amount_var.get()+","
                    self.data1["tax_no_due_app_no"] = self.work_data["tax_no_due_app_no"] +self.tax_no_due_app_no_var.get()+","
                    self.data1["tax_no_due_status"] = self.work_data["tax_no_due_status"] +self.tax_no_due_status_var.get()+","
                    self.data1["tax_no_due_time"] = self.work_data["tax_no_due_time"] + formatted_time + ","
                    self.data1["tax_no_due_date"] = self.work_data["tax_no_due_date"] +formatted_date + ","
                    self.data1["tax_no_due_priority"] = self.work_data["tax_no_due_priority"] +self.con_value(round(self.tax_no_due_scale.get()))+","
                    self.data1["tax_no_due_expiry_date"] = self.work_data["tax_no_due_expiry_date"] +self.tax_no_due_expiry_date_var.get()+","





                    # adding tax_no_due amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.tax_no_due_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    res = database.com_tax_no_due_entry(self.data, self.data1)
                    if res == True:
                        self.tax_no_due_top_level.destroy()
                        self.on_close_tax_no_due_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.tax_no_due_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.tax_no_due_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")





                    data = self.work_data["tax_no_due_amount"].split(',')
                    # removing old amount of tax_no_due
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of tax_no_due
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.tax_no_due_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    data = self.work_data["tax_no_due_amount"].split(',')
                    data[self.index] = self.tax_no_due_amount_entry.get()
                    data =",".join(data)
                    self.work_data["tax_no_due_amount"] = data


                    data = self.work_data["tax_no_due_app_no"].split(',')
                    data[self.index] = self.tax_no_due_app_no_var.get()
                    data =",".join(data)
                    self.work_data["tax_no_due_app_no"] = data

                    data = self.work_data["tax_no_due_status"].split(',')
                    data[self.index] = self.tax_no_due_status_var.get()
                    data =",".join(data)
                    self.work_data["tax_no_due_status"] = data

                    data = self.work_data["tax_no_due_priority"].split(',')
                    data[self.index] = self.con_value(round(self.tax_no_due_scale.get()))
                    data =",".join(data)
                    self.work_data["tax_no_due_priority"] = data

                    data = self.work_data["tax_no_due_expiry_date"].split(',')
                    data[self.index] = self.tax_no_due_expiry_date_var.get()
                    data =",".join(data)
                    self.work_data["tax_no_due_expiry_date"] = data
                    # messagebox.showinfo(parent=self.tax_no_due_top_level,title="",message=data)
                    res = database.com_tax_no_due_entry(self.data, self.work_data)
                    if res == True:
                        self.tax_no_due_top_level.destroy()
                        self.on_close_tax_no_due_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.tax_no_due_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def tax_no_due_combo_fun(self, event):
        if self.tax_no_due_combo_box.get() == "NEW ENTRY":
            self.tax_no_due_amount_var.set("")
            self.tax_no_due_app_no_var.set("")
            self.tax_no_due_status_var.set("1")
            self.tax_no_due_status_change()
            self.tax_no_due_entry_selection_var = "NEW ENTRY"
            self.tax_no_due_date_lbl.config(text="")
            self.tax_no_due_time_lbl.config(text="")
            self.tax_no_due_scale.set(0)
            self.tax_no_due_expiry_date_var.set("")


        # self.data[0]["tax_no_due_amount"]
        else:
            self.tax_no_due_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.tax_no_due_combo_box.get())-1
            amount = self.work_data["tax_no_due_amount"].split(",")
            app_no = self.work_data["tax_no_due_app_no"].split(",")
            status = self.work_data["tax_no_due_status"].split(",")
            date = self.work_data["tax_no_due_date"].split(",")
            time = self.work_data["tax_no_due_time"].split(",")
            priority = self.work_data["tax_no_due_priority"].split(",")
            tax_no_due_expiry = self.work_data["tax_no_due_expiry_date"].split(",")
            self.tax_no_due_amount_var.set(amount[int(self.tax_no_due_combo_box.get())-1])
            self.tax_no_due_app_no_var.set(app_no[int(self.tax_no_due_combo_box.get())-1])
            self.tax_no_due_status_var.set(status[int(self.tax_no_due_combo_box.get())-1])
            self.tax_no_due_date_lbl.config(text=date[int(self.tax_no_due_combo_box.get())-1])
            self.tax_no_due_time_lbl.config(text=time[int(self.tax_no_due_combo_box.get())-1])
            self.tax_no_due_scale.set(self.con_value_rev(priority[int(self.tax_no_due_combo_box.get())-1]))
            self.tax_no_due_expiry_date_var.set(tax_no_due_expiry[int(self.tax_no_due_combo_box.get())-1])
            if self.tax_no_due_status_var.get() == "0":
                self.tax_no_due_status_btn.config(image=self.pending_status_img)
            elif self.tax_no_due_status_var.get() == "1":
                self.tax_no_due_status_btn.config(image=self.completed_status_img)

    def tax_no_due_entry_delete_fun(self):
        if self.tax_no_due_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["tax_no_due_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])



            data = self.work_data["tax_no_due_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_no_due_amount"] = data

            data = self.work_data["tax_no_due_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_no_due_app_no"] = data

            data = self.work_data["tax_no_due_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_no_due_status"] = data

            data = self.work_data["tax_no_due_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_no_due_date"] = data

            data = self.work_data["tax_no_due_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_no_due_time"] = data

            data = self.work_data["tax_no_due_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_no_due_priority"] = data

            data = self.work_data["tax_no_due_expiry_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["tax_no_due_expiry_date"] = data

            res = database.com_tax_no_due_entry(self.data, self.work_data)
            if res == True:
                self.tax_no_due_top_level.destroy()
                self.on_close_tax_no_due_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.tax_no_due_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def tax_no_due_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.tax_no_due_update_scale_color(value)  # Update scale color based on value

    def convert_tax_no_due_app_no_to_uppercase(self):
        current_text = self.tax_no_due_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.tax_no_due_app_no_var.set(uppercase_text)




















    def open_reassignment_win(self):
        if not self.reassignment_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.reassignment_top_level_open = True
            self.reassignment_top_level = Toplevel()
            self.reassignment_top_level.protocol("WM_DELETE_WINDOW", self.on_close_reassignment_top_level)
            self.reassignment_top_level.configure(bg='#B39CD0')
            screen_width = self.reassignment_top_level.winfo_screenwidth()
            screen_height = self.reassignment_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.reassignment_top_level.title("RE ASSIGNMENT")
            self.reassignment_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.reassignment_top_level.winfo_screenwidth()
            screen_height = self.reassignment_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.reassignment_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.reassignment_top_level.resizable(False, False)
            self.reassignment_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\reassignment_bg.png"))
            Label(master=self.reassignment_top_level,
                  image=self.reassignment_bg_img).pack()

            self.reassignment_time_lbl = Label(self.reassignment_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.reassignment_time_lbl.place(x=75,y=51)

            self.reassignment_date_lbl = Label(self.reassignment_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.reassignment_date_lbl.place(x=195, y=51)

            self.reassignment_combo_box = ttk.Combobox(self.reassignment_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.reassignment_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.reassignment_scale = ttk.Scale(self.reassignment_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.reassignment_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.reassignment_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["reassignment_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.reassignment_combo_box['values'] = self.combo_values

            self.reassignment_combo_box.bind('<<ComboboxSelected>>', self.reassignment_combo_fun)
            self.reassignment_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.reassignment_amount_var = StringVar()
            self.reassignment_amount_entry = Entry(self.reassignment_top_level,
                                                 textvariable=self.reassignment_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.reassignment_amount_entry.place(x=60, y=125)







            self.re_assign_app_no_var = StringVar()
            self.re_assign_app_no_entry = Entry(self.reassignment_top_level,
                                                textvariable=self.re_assign_app_no_var,
                                                # state="disabled",
                                                # disabledbackground=self.color_1,
                                                validate="key",
                                                validatecommand=(self.main_root.register(self.validate_data),
                                                                 "%P"),
                                                bg=self.color_1, border=0,
                                                width=self.field_width_2,
                                                font=("Helvetica", self.font_size))
            self.re_assign_app_no_entry.place(x=60, y=195)
            self.re_assign_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_reassign_app_no_to_uppercase())

            self.re_assign_new_no_var = StringVar()
            self.re_assign_new_no_entry = Entry(self.reassignment_top_level,
                                                textvariable=self.re_assign_new_no_var,
                                                # state="disabled",
                                                # disabledbackground=self.color_1,
                                                validate="key",
                                                validatecommand=(self.main_root.register(self.validate_data),
                                                                 "%P"),
                                                bg=self.color_1, border=0,
                                                width=self.field_width_2,
                                                font=("Helvetica", self.font_size))
            self.re_assign_new_no_entry.place(x=60, y=265)
            self.re_assign_new_no_entry.bind('<KeyRelease>', lambda event: self.convert_re_assign_new_no_to_uppercase())

            self.valuation_and_taxes_var = StringVar()
            self.valuation_and_taxes_entry = Entry(self.reassignment_top_level,
                                         textvariable=self.valuation_and_taxes_var,
                                         # state="disabled",
                                         # disabledbackground=self.color_1,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_amount),
                                                          "%P"),
                                         bg=self.color_1, border=0,
                                         width=self.field_width_2,
                                         font=("Helvetica", self.font_size))
            self.valuation_and_taxes_entry.place(x=60, y=335)











            self.reassignment_status_var = StringVar()
            self.reassignment_status_var.set("0")
            self.reassignment_status_btn = Button(master=self.reassignment_top_level,
                                                textvariable=self.reassignment_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.reassignment_status_change,
                                                borderwidth=0
                                                )
            self.reassignment_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.reassignment_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_reassignment_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.reassignment_top_level,image=self.delete_but_img,
                   command=self.reassignment_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.reassignment_top_level.mainloop()

    def on_close_reassignment_top_level(self):
        self.reassignment_top_level_open = False
        self.reassignment_top_level.destroy()
        self.windows = "closed"

    def reassignment_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def reassignment_status_change(self):
        if self.reassignment_status_var.get() == "0":
            self.reassignment_status_btn.config(image=self.completed_status_img)
            self.reassignment_status_var.set("1")
            print(self.reassignment_status_var.get())
        elif self.reassignment_status_var.get() == "1":
            self.reassignment_status_btn.config(image=self.pending_status_img)
            self.reassignment_status_var.set("0")
            print(self.reassignment_status_var.get())

    def com_reassignment_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.reassignment_priority_var.get()))
        if self.reassignment_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.reassignment_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("reassignment_amount") == None:
                print("1")
                if self.reassignment_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["reassignment_amount"] = self.reassignment_amount_var.get()+","
                    self.data1["reassignment_status"] = self.reassignment_status_var.get()+","
                    self.data1["reassignment_time"] = formatted_time + ","
                    self.data1["reassignment_date"] = formatted_date + ","
                    self.data1["reassignment_priority"] = self.con_value(round(self.reassignment_scale.get()))+","
                    self.data1["reassignment_app_no"] = self.re_assign_app_no_var.get()+","
                    self.data1["reassignment_new_no"] = self.re_assign_new_no_var.get()+","
                    self.data1["reassignment_valuation_taxes"] = self.valuation_and_taxes_var.get()+","





                    # adding reassignment amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.reassignment_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_reassignment_entry(self.data, self.data1)
                    if res == True:
                        self.reassignment_top_level.destroy()
                        self.on_close_reassignment_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.reassignment_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("reassignment_amount") != None:
                print("2.0")
                if self.reassignment_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["reassignment_amount"] = self.work_data["reassignment_amount"] +self.reassignment_amount_var.get()+","
                    self.data1["reassignment_status"] = self.work_data["reassignment_status"] +self.reassignment_status_var.get()+","
                    self.data1["reassignment_time"] = self.work_data["reassignment_time"] + formatted_time + ","
                    self.data1["reassignment_date"] = self.work_data["reassignment_date"] +formatted_date + ","
                    self.data1["reassignment_priority"] = self.work_data["reassignment_priority"] +self.con_value(round(self.reassignment_scale.get()))+","

                    self.data1["reassignment_app_no"] = self.work_data["reassignment_app_no"] +self.re_assign_app_no_var.get()+","
                    self.data1["reassignment_new_no"] = self.work_data["reassignment_new_no"] +self.re_assign_new_no_var.get()+","
                    self.data1["reassignment_valuation_taxes"] = self.work_data["reassignment_valuation_taxes"] +self.valuation_and_taxes_var.get()+","





                    # adding reassignment amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.reassignment_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    res = database.com_reassignment_entry(self.data, self.data1)
                    if res == True:
                        self.reassignment_top_level.destroy()
                        self.on_close_reassignment_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.reassignment_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.reassignment_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")






                    data = self.work_data["reassignment_amount"].split(',')
                    # removing old amount of reassignment
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of reassignment
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.reassignment_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    data = self.work_data["reassignment_amount"].split(',')
                    data[self.index] = self.reassignment_amount_entry.get()
                    data =",".join(data)
                    self.work_data["reassignment_amount"] = data

                    data = self.work_data["reassignment_status"].split(',')
                    data[self.index] = self.reassignment_status_var.get()
                    data =",".join(data)
                    self.work_data["reassignment_status"] = data

                    data = self.work_data["reassignment_priority"].split(',')
                    data[self.index] = self.con_value(round(self.reassignment_scale.get()))
                    data =",".join(data)
                    self.work_data["reassignment_priority"] = data

                    data = self.work_data["reassignment_app_no"].split(',')
                    data[self.index] = self.re_assign_app_no_var.get()
                    data =",".join(data)
                    self.work_data["reassignment_app_no"] = data

                    data = self.work_data["reassignment_new_no"].split(',')
                    data[self.index] = self.re_assign_new_no_var.get()
                    data =",".join(data)
                    self.work_data["reassignment_new_no"] = data

                    data = self.work_data["reassignment_valuation_taxes"].split(',')
                    data[self.index] = self.valuation_and_taxes_var.get()
                    data =",".join(data)
                    self.work_data["reassignment_valuation_taxes"] = data

                    # messagebox.showinfo(parent=self.reassignment_top_level,title="",message=data)
                    res = database.com_reassignment_entry(self.data, self.work_data)
                    if res == True:
                        self.reassignment_top_level.destroy()
                        self.on_close_reassignment_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.reassignment_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def reassignment_combo_fun(self, event):
        if self.reassignment_combo_box.get() == "NEW ENTRY":
            self.reassignment_amount_var.set("")
            self.reassignment_status_var.set("1")
            self.reassignment_status_change()
            self.reassignment_entry_selection_var = "NEW ENTRY"
            self.reassignment_date_lbl.config(text="")
            self.reassignment_time_lbl.config(text="")
            self.reassignment_scale.set(0)
            self.re_assign_app_no_var.set("")
            self.re_assign_new_no_var.set("")
            self.valuation_and_taxes_var.set("")


        # self.data[0]["reassignment_amount"]
        else:
            self.reassignment_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.reassignment_combo_box.get())-1
            amount = self.work_data["reassignment_amount"].split(",")
            status = self.work_data["reassignment_status"].split(",")
            date = self.work_data["reassignment_date"].split(",")
            time = self.work_data["reassignment_time"].split(",")
            priority = self.work_data["reassignment_priority"].split(",")
            app_no = self.work_data["reassignment_app_no"].split(",")
            new_no = self.work_data["reassignment_new_no"].split(",")
            valuation_and_taxes = self.work_data["reassignment_valuation_taxes"].split(",")
            self.reassignment_amount_var.set(amount[int(self.reassignment_combo_box.get())-1])
            self.reassignment_status_var.set(status[int(self.reassignment_combo_box.get())-1])
            self.reassignment_date_lbl.config(text=date[int(self.reassignment_combo_box.get())-1])
            self.reassignment_time_lbl.config(text=time[int(self.reassignment_combo_box.get())-1])
            self.reassignment_scale.set(self.con_value_rev(priority[int(self.reassignment_combo_box.get())-1]))

            self.re_assign_app_no_var.set(app_no[int(self.reassignment_combo_box.get())-1])
            self.re_assign_new_no_var.set(new_no[int(self.reassignment_combo_box.get())-1])
            self.valuation_and_taxes_var.set(valuation_and_taxes[int(self.reassignment_combo_box.get())-1])
            if self.reassignment_status_var.get() == "0":
                self.reassignment_status_btn.config(image=self.pending_status_img)
            elif self.reassignment_status_var.get() == "1":
                self.reassignment_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.reassignment_top_level, title="",message="")

    def reassignment_entry_delete_fun(self):
        if self.reassignment_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)





            # these three line of code, subtract delete work amount from total
            data = self.work_data["reassignment_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["reassignment_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_amount"] = data

            data = self.work_data["reassignment_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_status"] = data

            data = self.work_data["reassignment_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_date"] = data

            data = self.work_data["reassignment_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_time"] = data

            data = self.work_data["reassignment_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_priority"] = data

            data = self.work_data["reassignment_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_app_no"] = data

            data = self.work_data["reassignment_new_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_new_no"] = data

            data = self.work_data["reassignment_valuation_taxes"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["reassignment_valuation_taxes"] = data

            res = database.com_reassignment_entry(self.data, self.work_data)
            if res == True:
                self.reassignment_top_level.destroy()
                self.on_close_reassignment_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.reassignment_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def reassignment_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.reassignment_update_scale_color(value)  # Update scale color based on value























    def open_noc_sent_win(self):
        if not self.noc_sent_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.noc_sent_top_level_open = True
            self.noc_sent_top_level = Toplevel()
            self.noc_sent_top_level.protocol("WM_DELETE_WINDOW", self.on_close_noc_sent_top_level)
            self.noc_sent_top_level.configure(bg='#B39CD0')
            screen_width = self.noc_sent_top_level.winfo_screenwidth()
            screen_height = self.noc_sent_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.noc_sent_top_level.title("NOC SENT")
            self.noc_sent_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.noc_sent_top_level.winfo_screenwidth()
            screen_height = self.noc_sent_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.noc_sent_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.noc_sent_top_level.resizable(False, False)
            self.noc_sent_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\noc_sent_bg.png"))
            Label(master=self.noc_sent_top_level,
                  image=self.noc_sent_bg_img).pack()

            self.noc_sent_time_lbl = Label(self.noc_sent_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.noc_sent_time_lbl.place(x=75,y=51)

            self.noc_sent_date_lbl = Label(self.noc_sent_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.noc_sent_date_lbl.place(x=195, y=51)

            self.noc_sent_combo_box = ttk.Combobox(self.noc_sent_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.noc_sent_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.noc_sent_scale = ttk.Scale(self.noc_sent_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.noc_sent_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.noc_sent_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["noc_sent_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.noc_sent_combo_box['values'] = self.combo_values

            self.noc_sent_combo_box.bind('<<ComboboxSelected>>', self.noc_sent_combo_fun)
            self.noc_sent_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.noc_sent_amount_var = StringVar()
            self.noc_sent_amount_entry = Entry(self.noc_sent_top_level,
                                                 textvariable=self.noc_sent_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.noc_sent_amount_entry.place(x=60, y=125)







            self.noc_sent_state_var = StringVar()
            self.noc_sent_state_entry = Entry(self.noc_sent_top_level,
                                                textvariable=self.noc_sent_state_var,
                                                # state="disabled",
                                                # disabledbackground=self.color_1,
                                                validate="key",
                                                validatecommand=(self.main_root.register(self.validate_name),
                                                                 "%P"),
                                                bg=self.color_1, border=0,
                                                width=self.field_width_2,
                                                font=("Helvetica", self.font_size))
            self.noc_sent_state_entry.place(x=60, y=195)
            self.noc_sent_state_entry.bind('<KeyRelease>', lambda event: self.convert_noc_sent_state_to_uppercase())

            self.noc_sent_district_var = StringVar()
            self.noc_sent_district_entry = Entry(self.noc_sent_top_level,
                                                textvariable=self.noc_sent_district_var,
                                                # state="disabled",
                                                # disabledbackground=self.color_1,
                                                validate="key",
                                                validatecommand=(self.main_root.register(self.validate_name),
                                                                 "%P"),
                                                bg=self.color_1, border=0,
                                                width=self.field_width_2,
                                                font=("Helvetica", self.font_size))
            self.noc_sent_district_entry.place(x=60, y=265)
            self.noc_sent_district_entry.bind('<KeyRelease>', lambda event: self.convert_noc_sent_district_to_uppercase())

            self.noc_sent_app_no_var = StringVar()
            self.noc_sent_app_no_entry = Entry(self.noc_sent_top_level,
                                         textvariable=self.noc_sent_app_no_var,
                                         # state="disabled",
                                         # disabledbackground=self.color_1,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data),
                                                          "%P"),
                                         bg=self.color_1, border=0,
                                         width=self.field_width_2,
                                         font=("Helvetica", self.font_size))
            self.noc_sent_app_no_entry.place(x=60, y=335)
            self.noc_sent_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_noc_sent_app_no_to_uppercase())











            self.noc_sent_status_var = StringVar()
            self.noc_sent_status_var.set("0")
            self.noc_sent_status_btn = Button(master=self.noc_sent_top_level,
                                                textvariable=self.noc_sent_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.noc_sent_status_change,
                                                borderwidth=0
                                                )
            self.noc_sent_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.noc_sent_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_noc_sent_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.noc_sent_top_level,image=self.delete_but_img,
                   command=self.noc_sent_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.noc_sent_top_level.mainloop()

    def on_close_noc_sent_top_level(self):
        self.noc_sent_top_level_open = False
        self.noc_sent_top_level.destroy()
        self.windows = "closed"

    def noc_sent_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def noc_sent_status_change(self):
        if self.noc_sent_status_var.get() == "0":
            self.noc_sent_status_btn.config(image=self.completed_status_img)
            self.noc_sent_status_var.set("1")
            print(self.noc_sent_status_var.get())
        elif self.noc_sent_status_var.get() == "1":
            self.noc_sent_status_btn.config(image=self.pending_status_img)
            self.noc_sent_status_var.set("0")
            print(self.noc_sent_status_var.get())

    def com_noc_sent_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.noc_sent_priority_var.get()))
        if self.noc_sent_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.noc_sent_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("noc_sent_amount") == None:
                print("1")
                if self.noc_sent_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["noc_sent_amount"] = self.noc_sent_amount_var.get()+","
                    self.data1["noc_sent_status"] = self.noc_sent_status_var.get()+","
                    self.data1["noc_sent_time"] = formatted_time + ","
                    self.data1["noc_sent_date"] = formatted_date + ","
                    self.data1["noc_sent_priority"] = self.con_value(round(self.noc_sent_scale.get()))+","
                    self.data1["noc_sent_app_no"] = self.noc_sent_app_no_var.get()+","
                    self.data1["noc_sent_state"] = self.noc_sent_state_var.get()+","
                    self.data1["noc_sent_district"] = self.noc_sent_district_var.get()+","





                    # adding noc_sent amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.noc_sent_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_noc_sent_entry(self.data, self.data1,)
                    if res == True:
                        self.noc_sent_top_level.destroy()
                        self.on_close_noc_sent_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.noc_sent_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("noc_sent_amount") != None:
                print("2.0")
                if self.noc_sent_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["noc_sent_amount"] = self.work_data["noc_sent_amount"] +self.noc_sent_amount_var.get()+","
                    self.data1["noc_sent_status"] = self.work_data["noc_sent_status"] +self.noc_sent_status_var.get()+","
                    self.data1["noc_sent_time"] = self.work_data["noc_sent_time"] + formatted_time + ","
                    self.data1["noc_sent_date"] = self.work_data["noc_sent_date"] +formatted_date + ","
                    self.data1["noc_sent_priority"] = self.work_data["noc_sent_priority"] +self.con_value(round(self.noc_sent_scale.get()))+","

                    self.data1["noc_sent_app_no"] = self.work_data["noc_sent_app_no"] +self.noc_sent_app_no_var.get()+","
                    self.data1["noc_sent_district"] = self.work_data["noc_sent_district"] +self.noc_sent_district_var.get()+","
                    self.data1["noc_sent_state"] = self.work_data["noc_sent_state"] +self.noc_sent_state_var.get()+","





                    # adding noc_sent amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.noc_sent_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    res = database.com_noc_sent_entry(self.data, self.data1, )
                    if res == True:
                        self.noc_sent_top_level.destroy()
                        self.on_close_noc_sent_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.noc_sent_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.noc_sent_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")






                    data = self.work_data["noc_sent_amount"].split(',')
                    # removing old amount of noc_sent
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of noc_sent
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.noc_sent_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    data = self.work_data["noc_sent_amount"].split(',')
                    data[self.index] = self.noc_sent_amount_entry.get()
                    data =",".join(data)
                    self.work_data["noc_sent_amount"] = data

                    data = self.work_data["noc_sent_status"].split(',')
                    data[self.index] = self.noc_sent_status_var.get()
                    data =",".join(data)
                    self.work_data["noc_sent_status"] = data

                    data = self.work_data["noc_sent_priority"].split(',')
                    data[self.index] = self.con_value(round(self.noc_sent_scale.get()))
                    data =",".join(data)
                    self.work_data["noc_sent_priority"] = data

                    data = self.work_data["noc_sent_app_no"].split(',')
                    data[self.index] = self.noc_sent_app_no_var.get()
                    data =",".join(data)
                    self.work_data["noc_sent_app_no"] = data

                    data = self.work_data["noc_sent_state"].split(',')
                    data[self.index] = self.noc_sent_state_var.get()
                    data =",".join(data)
                    self.work_data["noc_sent_state"] = data

                    data = self.work_data["noc_sent_district"].split(',')
                    data[self.index] = self.noc_sent_district_var.get()
                    data =",".join(data)
                    self.work_data["noc_sent_district"] = data

                    # messagebox.showinfo(parent=self.noc_sent_top_level,title="",message=data)
                    res = database.com_noc_sent_entry(self.data, self.work_data)
                    if res == True:
                        self.noc_sent_top_level.destroy()
                        self.on_close_noc_sent_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.noc_sent_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def noc_sent_combo_fun(self, event):
        if self.noc_sent_combo_box.get() == "NEW ENTRY":
            self.noc_sent_amount_var.set("")
            self.noc_sent_status_var.set("1")
            self.noc_sent_status_change()
            self.noc_sent_entry_selection_var = "NEW ENTRY"
            self.noc_sent_date_lbl.config(text="")
            self.noc_sent_time_lbl.config(text="")
            self.noc_sent_scale.set(0)
            self.noc_sent_app_no_var.set("")
            self.noc_sent_district_var.set("")
            self.noc_sent_state_var.set("")


        # self.data[0]["noc_sent_amount"]
        else:
            self.noc_sent_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.noc_sent_combo_box.get())-1
            amount = self.work_data["noc_sent_amount"].split(",")
            status = self.work_data["noc_sent_status"].split(",")
            date = self.work_data["noc_sent_date"].split(",")
            time = self.work_data["noc_sent_time"].split(",")
            priority = self.work_data["noc_sent_priority"].split(",")
            app_no = self.work_data["noc_sent_app_no"].split(",")
            state = self.work_data["noc_sent_state"].split(",")
            district = self.work_data["noc_sent_district"].split(",")
            self.noc_sent_amount_var.set(amount[int(self.noc_sent_combo_box.get())-1])
            self.noc_sent_status_var.set(status[int(self.noc_sent_combo_box.get())-1])
            self.noc_sent_date_lbl.config(text=date[int(self.noc_sent_combo_box.get())-1])
            self.noc_sent_time_lbl.config(text=time[int(self.noc_sent_combo_box.get())-1])
            self.noc_sent_scale.set(self.con_value_rev(priority[int(self.noc_sent_combo_box.get())-1]))

            self.noc_sent_app_no_var.set(app_no[int(self.noc_sent_combo_box.get())-1])
            self.noc_sent_state_var.set(state[int(self.noc_sent_combo_box.get())-1])
            self.noc_sent_district_var.set(district[int(self.noc_sent_combo_box.get())-1])
            if self.noc_sent_status_var.get() == "0":
                self.noc_sent_status_btn.config(image=self.pending_status_img)
            elif self.noc_sent_status_var.get() == "1":
                self.noc_sent_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.noc_sent_top_level, title="",message="")

    def noc_sent_entry_delete_fun(self):
        if self.noc_sent_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)





            # these three line of code, subtract delete work amount from total
            data = self.work_data["noc_sent_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["noc_sent_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_amount"] = data

            data = self.work_data["noc_sent_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_status"] = data

            data = self.work_data["noc_sent_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_date"] = data

            data = self.work_data["noc_sent_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_time"] = data

            data = self.work_data["noc_sent_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_priority"] = data

            data = self.work_data["noc_sent_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_app_no"] = data

            data = self.work_data["noc_sent_district"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_district"] = data

            data = self.work_data["noc_sent_state"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_sent_state"] = data

            res = database.com_noc_sent_entry(self.data, self.work_data)
            if res == True:
                self.noc_sent_top_level.destroy()
                self.on_close_noc_sent_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.noc_sent_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def noc_sent_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.noc_sent_update_scale_color(value)  # Update scale color based on value





























    def open_noc_accept_win(self):
        if not self.noc_accept_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.noc_accept_top_level_open = True
            self.noc_accept_top_level = Toplevel()
            self.noc_accept_top_level.protocol("WM_DELETE_WINDOW", self.on_close_noc_accept_top_level)
            self.noc_accept_top_level.configure(bg='#B39CD0')
            screen_width = self.noc_accept_top_level.winfo_screenwidth()
            screen_height = self.noc_accept_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.noc_accept_top_level.title("NOC ACCEPT")
            self.noc_accept_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.noc_accept_top_level.winfo_screenwidth()
            screen_height = self.noc_accept_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.noc_accept_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.noc_accept_top_level.resizable(False, False)
            self.noc_accept_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\noc_accept_bg.png"))
            Label(master=self.noc_accept_top_level,
                  image=self.noc_accept_bg_img).pack()

            self.noc_accept_time_lbl = Label(self.noc_accept_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.noc_accept_time_lbl.place(x=75,y=51)

            self.noc_accept_date_lbl = Label(self.noc_accept_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.noc_accept_date_lbl.place(x=195, y=51)

            self.noc_accept_combo_box = ttk.Combobox(self.noc_accept_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.noc_accept_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.noc_accept_scale = ttk.Scale(self.noc_accept_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.noc_accept_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.noc_accept_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["noc_accept_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.noc_accept_combo_box['values'] = self.combo_values

            self.noc_accept_combo_box.bind('<<ComboboxSelected>>', self.noc_accept_combo_fun)
            self.noc_accept_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.noc_accept_amount_var = StringVar()
            self.noc_accept_amount_entry = Entry(self.noc_accept_top_level,
                                                 textvariable=self.noc_accept_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.noc_accept_amount_entry.place(x=60, y=125)







            self.noc_accept_state_var = StringVar()
            self.noc_accept_state_entry = Entry(self.noc_accept_top_level,
                                                textvariable=self.noc_accept_state_var,
                                                # state="disabled",
                                                # disabledbackground=self.color_1,
                                                validate="key",
                                                validatecommand=(self.main_root.register(self.validate_name),
                                                                 "%P"),
                                                bg=self.color_1, border=0,
                                                width=self.field_width_2,
                                                font=("Helvetica", self.font_size))
            self.noc_accept_state_entry.place(x=60, y=195)
            self.noc_accept_state_entry.bind('<KeyRelease>', lambda event: self.convert_noc_accept_state_to_uppercase())

            self.noc_accept_district_var = StringVar()
            self.noc_accept_district_entry = Entry(self.noc_accept_top_level,
                                                textvariable=self.noc_accept_district_var,
                                                # state="disabled",
                                                # disabledbackground=self.color_1,
                                                validate="key",
                                                validatecommand=(self.main_root.register(self.validate_name),
                                                                 "%P"),
                                                bg=self.color_1, border=0,
                                                width=self.field_width_2,
                                                font=("Helvetica", self.font_size))
            self.noc_accept_district_entry.place(x=60, y=265)
            self.noc_accept_district_entry.bind('<KeyRelease>', lambda event: self.convert_noc_accept_district_to_uppercase())

            self.noc_accept_app_no_var = StringVar()
            self.noc_accept_app_no_entry = Entry(self.noc_accept_top_level,
                                         textvariable=self.noc_accept_app_no_var,
                                         # state="disabled",
                                         # disabledbackground=self.color_1,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data),
                                                          "%P"),
                                         bg=self.color_1, border=0,
                                         width=self.field_width_2,
                                         font=("Helvetica", self.font_size))
            self.noc_accept_app_no_entry.place(x=60, y=335)
            self.noc_accept_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_noc_accept_app_no_to_uppercase())











            self.noc_accept_status_var = StringVar()
            self.noc_accept_status_var.set("0")
            self.noc_accept_status_btn = Button(master=self.noc_accept_top_level,
                                                textvariable=self.noc_accept_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.noc_accept_status_change,
                                                borderwidth=0
                                                )
            self.noc_accept_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.noc_accept_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_noc_accept_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.noc_accept_top_level,image=self.delete_but_img,
                   command=self.noc_accept_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.noc_accept_top_level.mainloop()

    def on_close_noc_accept_top_level(self):
        self.noc_accept_top_level_open = False
        self.noc_accept_top_level.destroy()
        self.windows = "closed"

    def noc_accept_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def noc_accept_status_change(self):
        if self.noc_accept_status_var.get() == "0":
            self.noc_accept_status_btn.config(image=self.completed_status_img)
            self.noc_accept_status_var.set("1")
            print(self.noc_accept_status_var.get())
        elif self.noc_accept_status_var.get() == "1":
            self.noc_accept_status_btn.config(image=self.pending_status_img)
            self.noc_accept_status_var.set("0")
            print(self.noc_accept_status_var.get())

    def com_noc_accept_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.noc_accept_priority_var.get()))
        if self.noc_accept_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.noc_accept_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("noc_accept_amount") == None:
                print("1")
                if self.noc_accept_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["noc_accept_amount"] = self.noc_accept_amount_var.get()+","
                    self.data1["noc_accept_status"] = self.noc_accept_status_var.get()+","
                    self.data1["noc_accept_time"] = formatted_time + ","
                    self.data1["noc_accept_date"] = formatted_date + ","
                    self.data1["noc_accept_priority"] = self.con_value(round(self.noc_accept_scale.get()))+","
                    self.data1["noc_accept_app_no"] = self.noc_accept_app_no_var.get()+","
                    self.data1["noc_accept_state"] = self.noc_accept_state_var.get()+","
                    self.data1["noc_accept_district"] = self.noc_accept_district_var.get()+","





                    # adding noc_accept amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.noc_accept_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_noc_accept_entry(self.data, self.data1,)
                    if res == True:
                        self.noc_accept_top_level.destroy()
                        self.on_close_noc_accept_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.noc_accept_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("noc_accept_amount") != None:
                print("2.0")
                if self.noc_accept_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["noc_accept_amount"] = self.work_data["noc_accept_amount"] +self.noc_accept_amount_var.get()+","
                    self.data1["noc_accept_status"] = self.work_data["noc_accept_status"] +self.noc_accept_status_var.get()+","
                    self.data1["noc_accept_time"] = self.work_data["noc_accept_time"] + formatted_time + ","
                    self.data1["noc_accept_date"] = self.work_data["noc_accept_date"] +formatted_date + ","
                    self.data1["noc_accept_priority"] = self.work_data["noc_accept_priority"] +self.con_value(round(self.noc_accept_scale.get()))+","

                    self.data1["noc_accept_app_no"] = self.work_data["noc_accept_app_no"] +self.noc_accept_app_no_var.get()+","
                    self.data1["noc_accept_district"] = self.work_data["noc_accept_district"] +self.noc_accept_district_var.get()+","
                    self.data1["noc_accept_state"] = self.work_data["noc_accept_state"] +self.noc_accept_state_var.get()+","





                    # adding noc_accept amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.noc_accept_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    res = database.com_noc_accept_entry(self.data, self.data1)
                    if res == True:
                        self.noc_accept_top_level.destroy()
                        self.on_close_noc_accept_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.noc_accept_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.noc_accept_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")






                    data = self.work_data["noc_accept_amount"].split(',')
                    # removing old amount of noc_accept
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of noc_accept
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.noc_accept_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    data = self.work_data["noc_accept_amount"].split(',')
                    data[self.index] = self.noc_accept_amount_entry.get()
                    data =",".join(data)
                    self.work_data["noc_accept_amount"] = data

                    data = self.work_data["noc_accept_status"].split(',')
                    data[self.index] = self.noc_accept_status_var.get()
                    data =",".join(data)
                    self.work_data["noc_accept_status"] = data

                    data = self.work_data["noc_accept_priority"].split(',')
                    data[self.index] = self.con_value(round(self.noc_accept_scale.get()))
                    data =",".join(data)
                    self.work_data["noc_accept_priority"] = data

                    data = self.work_data["noc_accept_app_no"].split(',')
                    data[self.index] = self.noc_accept_app_no_var.get()
                    data =",".join(data)
                    self.work_data["noc_accept_app_no"] = data

                    data = self.work_data["noc_accept_state"].split(',')
                    data[self.index] = self.noc_accept_state_var.get()
                    data =",".join(data)
                    self.work_data["noc_accept_state"] = data

                    data = self.work_data["noc_accept_district"].split(',')
                    data[self.index] = self.noc_accept_district_var.get()
                    data =",".join(data)
                    self.work_data["noc_accept_district"] = data

                    # messagebox.showinfo(parent=self.noc_accept_top_level,title="",message=data)
                    res = database.com_noc_accept_entry(self.data, self.work_data)
                    if res == True:
                        self.noc_accept_top_level.destroy()
                        self.on_close_noc_accept_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.noc_accept_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def noc_accept_combo_fun(self, event):
        if self.noc_accept_combo_box.get() == "NEW ENTRY":
            self.noc_accept_amount_var.set("")
            self.noc_accept_status_var.set("1")
            self.noc_accept_status_change()
            self.noc_accept_entry_selection_var = "NEW ENTRY"
            self.noc_accept_date_lbl.config(text="")
            self.noc_accept_time_lbl.config(text="")
            self.noc_accept_scale.set(0)
            self.noc_accept_app_no_var.set("")
            self.noc_accept_district_var.set("")
            self.noc_accept_state_var.set("")


        # self.data[0]["noc_accept_amount"]
        else:
            self.noc_accept_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.noc_accept_combo_box.get())-1
            amount = self.work_data["noc_accept_amount"].split(",")
            status = self.work_data["noc_accept_status"].split(",")
            date = self.work_data["noc_accept_date"].split(",")
            time = self.work_data["noc_accept_time"].split(",")
            priority = self.work_data["noc_accept_priority"].split(",")
            app_no = self.work_data["noc_accept_app_no"].split(",")
            state = self.work_data["noc_accept_state"].split(",")
            district = self.work_data["noc_accept_district"].split(",")
            self.noc_accept_amount_var.set(amount[int(self.noc_accept_combo_box.get())-1])
            self.noc_accept_status_var.set(status[int(self.noc_accept_combo_box.get())-1])
            self.noc_accept_date_lbl.config(text=date[int(self.noc_accept_combo_box.get())-1])
            self.noc_accept_time_lbl.config(text=time[int(self.noc_accept_combo_box.get())-1])
            self.noc_accept_scale.set(self.con_value_rev(priority[int(self.noc_accept_combo_box.get())-1]))

            self.noc_accept_app_no_var.set(app_no[int(self.noc_accept_combo_box.get())-1])
            self.noc_accept_state_var.set(state[int(self.noc_accept_combo_box.get())-1])
            self.noc_accept_district_var.set(district[int(self.noc_accept_combo_box.get())-1])
            if self.noc_accept_status_var.get() == "0":
                self.noc_accept_status_btn.config(image=self.pending_status_img)
            elif self.noc_accept_status_var.get() == "1":
                self.noc_accept_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.noc_accept_top_level, title="",message="")

    def noc_accept_entry_delete_fun(self):
        if self.noc_accept_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)





            # these three line of code, subtract delete work amount from total
            data = self.work_data["noc_accept_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["noc_accept_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_amount"] = data

            data = self.work_data["noc_accept_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_status"] = data

            data = self.work_data["noc_accept_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_date"] = data

            data = self.work_data["noc_accept_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_time"] = data

            data = self.work_data["noc_accept_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_priority"] = data

            data = self.work_data["noc_accept_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_app_no"] = data

            data = self.work_data["noc_accept_district"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_district"] = data

            data = self.work_data["noc_accept_state"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["noc_accept_state"] = data

            res = database.com_noc_accept_entry(self.data, self.work_data)
            if res == True:
                self.noc_accept_top_level.destroy()
                self.on_close_noc_accept_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.noc_accept_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def noc_accept_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.noc_accept_update_scale_color(value)  # Update scale color based on value







































    def open_pb_surrender_win(self):
        if not self.pb_surrender_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.pb_surrender_top_level_open = True
            self.pb_surrender_top_level = Toplevel()
            self.pb_surrender_top_level.protocol("WM_DELETE_WINDOW", self.on_close_pb_surrender_top_level)
            self.pb_surrender_top_level.configure(bg='#B39CD0')
            screen_width = self.pb_surrender_top_level.winfo_screenwidth()
            screen_height = self.pb_surrender_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.pb_surrender_top_level.title("PB SURRENDER")
            self.pb_surrender_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.pb_surrender_top_level.winfo_screenwidth()
            screen_height = self.pb_surrender_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.pb_surrender_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.pb_surrender_top_level.resizable(False, False)
            self.pb_surrender_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\pb_surrender_bg.png"))
            Label(master=self.pb_surrender_top_level,
                  image=self.pb_surrender_bg_img).pack()

            self.pb_surrender_time_lbl = Label(self.pb_surrender_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.pb_surrender_time_lbl.place(x=75,y=51)

            self.pb_surrender_date_lbl = Label(self.pb_surrender_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.pb_surrender_date_lbl.place(x=195, y=51)

            self.pb_surrender_combo_box = ttk.Combobox(self.pb_surrender_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.pb_surrender_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.pb_surrender_scale = ttk.Scale(self.pb_surrender_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.pb_surrender_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.pb_surrender_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["pb_surrender_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.pb_surrender_combo_box['values'] = self.combo_values

            self.pb_surrender_combo_box.bind('<<ComboboxSelected>>', self.pb_surrender_combo_fun)
            self.pb_surrender_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.pb_surrender_amount_var = StringVar()
            self.pb_surrender_amount_entry = Entry(self.pb_surrender_top_level,
                                                 textvariable=self.pb_surrender_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.pb_surrender_amount_entry.place(x=60, y=125)

            self.pb_surrender_app_no_var = StringVar()
            self.pb_surrender_app_no_entry = Entry(self.pb_surrender_top_level,
                                         textvariable=self.pb_surrender_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.pb_surrender_app_no_entry.place(x=60, y=196)
            self.pb_surrender_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_pb_surrender_app_no_to_uppercase())

            self.pb_surrender_status_var = StringVar()
            self.pb_surrender_status_var.set("0")
            self.pb_surrender_status_btn = Button(master=self.pb_surrender_top_level,
                                                textvariable=self.pb_surrender_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.pb_surrender_status_change,
                                                borderwidth=0
                                                )
            self.pb_surrender_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.pb_surrender_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_pb_surrender_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.pb_surrender_top_level,image=self.delete_but_img,
                   command=self.pb_surrender_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.pb_surrender_top_level.mainloop()

    def on_close_pb_surrender_top_level(self):
        self.pb_surrender_top_level_open = False
        self.pb_surrender_top_level.destroy()
        self.windows = "closed"

    def pb_surrender_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def pb_surrender_status_change(self):
        if self.pb_surrender_status_var.get() == "0":
            self.pb_surrender_status_btn.config(image=self.completed_status_img)
            self.pb_surrender_status_var.set("1")
            print(self.pb_surrender_status_var.get())
        elif self.pb_surrender_status_var.get() == "1":
            self.pb_surrender_status_btn.config(image=self.pending_status_img)
            self.pb_surrender_status_var.set("0")
            print(self.pb_surrender_status_var.get())

    def com_pb_surrender_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.pb_surrender_priority_var.get()))
        if self.pb_surrender_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.pb_surrender_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("pb_surrender_amount") == None:
                print("1")
                if self.pb_surrender_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["pb_surrender_amount"] = self.pb_surrender_amount_var.get()+","
                    self.data1["pb_surrender_app_no"] = self.pb_surrender_app_no_var.get()+","
                    self.data1["pb_surrender_status"] = self.pb_surrender_status_var.get()+","
                    self.data1["pb_surrender_time"] = formatted_time + ","
                    self.data1["pb_surrender_date"] = formatted_date + ","
                    self.data1["pb_surrender_priority"] = self.con_value(round(self.pb_surrender_scale.get()))+","





                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_surrender_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_pb_surrender_entry(self.data, self.data1)
                    if res == True:
                        self.pb_surrender_top_level.destroy()
                        self.on_close_pb_surrender_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_surrender_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("pb_surrender_amount") != None:
                print("2.0")
                if self.pb_surrender_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["pb_surrender_amount"] = self.work_data["pb_surrender_amount"] +self.pb_surrender_amount_var.get()+","
                    self.data1["pb_surrender_app_no"] = self.work_data["pb_surrender_app_no"] +self.pb_surrender_app_no_var.get()+","
                    self.data1["pb_surrender_status"] = self.work_data["pb_surrender_status"] +self.pb_surrender_status_var.get()+","
                    self.data1["pb_surrender_time"] = self.work_data["pb_surrender_time"] + formatted_time + ","
                    self.data1["pb_surrender_date"] = self.work_data["pb_surrender_date"] +formatted_date + ","
                    self.data1["pb_surrender_priority"] = self.work_data["pb_surrender_priority"] +self.con_value(round(self.pb_surrender_scale.get()))+","






                    # adding redispatch amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_surrender_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    res = database.com_pb_surrender_entry(self.data, self.data1)
                    if res == True:
                        self.pb_surrender_top_level.destroy()
                        self.on_close_pb_surrender_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_surrender_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.pb_surrender_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["pb_surrender_amount"].split(',')
                    # removing old amount of pb_surrender
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of pb_surrender
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pb_surrender_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    data = self.work_data["pb_surrender_amount"].split(',')
                    data[self.index] = self.pb_surrender_amount_entry.get()
                    data =",".join(data)
                    self.work_data["pb_surrender_amount"] = data

                    data = self.work_data["pb_surrender_app_no"].split(',')
                    data[self.index] = self.pb_surrender_app_no_var.get()
                    data =",".join(data)
                    self.work_data["pb_surrender_app_no"] = data

                    data = self.work_data["pb_surrender_status"].split(',')
                    data[self.index] = self.pb_surrender_status_var.get()
                    data =",".join(data)
                    self.work_data["pb_surrender_status"] = data

                    data = self.work_data["pb_surrender_priority"].split(',')
                    data[self.index] = self.con_value(round(self.pb_surrender_scale.get()))
                    data =",".join(data)
                    self.work_data["pb_surrender_priority"] = data
                    # messagebox.showinfo(parent=self.pb_surrender_top_level,title="",message=data)
                    res = database.com_pb_surrender_entry(self.data, self.work_data)
                    if res == True:
                        self.pb_surrender_top_level.destroy()
                        self.on_close_pb_surrender_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pb_surrender_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def pb_surrender_combo_fun(self, event):
        if self.pb_surrender_combo_box.get() == "NEW ENTRY":
            self.pb_surrender_amount_var.set("")
            self.pb_surrender_app_no_var.set("")
            self.pb_surrender_status_var.set("1")
            self.pb_surrender_status_change()
            self.pb_surrender_entry_selection_var = "NEW ENTRY"
            self.pb_surrender_date_lbl.config(text="")
            self.pb_surrender_time_lbl.config(text="")
            self.pb_surrender_scale.set(0)


        # self.data[0]["pb_surrender_amount"]
        else:
            self.pb_surrender_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.pb_surrender_combo_box.get())-1
            amount = self.data1["pb_surrender_amount"].split(",")
            app_no = self.data1["pb_surrender_app_no"].split(",")
            status = self.data1["pb_surrender_status"].split(",")
            date = self.data1["pb_surrender_date"].split(",")
            time = self.data1["pb_surrender_time"].split(",")
            priority = self.data1["pb_surrender_priority"].split(",")
            self.pb_surrender_amount_var.set(amount[int(self.pb_surrender_combo_box.get())-1])
            self.pb_surrender_app_no_var.set(app_no[int(self.pb_surrender_combo_box.get())-1])
            self.pb_surrender_status_var.set(status[int(self.pb_surrender_combo_box.get())-1])
            self.pb_surrender_date_lbl.config(text=date[int(self.pb_surrender_combo_box.get())-1])
            self.pb_surrender_time_lbl.config(text=time[int(self.pb_surrender_combo_box.get())-1])
            self.pb_surrender_scale.set(self.con_value_rev(priority[int(self.pb_surrender_combo_box.get())-1]))
            if self.pb_surrender_status_var.get() == "0":
                self.pb_surrender_status_btn.config(image=self.pending_status_img)
            elif self.pb_surrender_status_var.get() == "1":
                self.pb_surrender_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.pb_surrender_top_level, title="",message="")

    def pb_surrender_entry_delete_fun(self):
        if self.pb_surrender_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["pb_surrender_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["pb_surrender_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_surrender_amount"] = data

            data = self.work_data["pb_surrender_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_surrender_app_no"] = data

            data = self.work_data["pb_surrender_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_surrender_status"] = data

            data = self.work_data["pb_surrender_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_surrender_date"] = data

            data = self.work_data["pb_surrender_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_surrender_time"] = data

            data = self.work_data["pb_surrender_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pb_surrender_priority"] = data

            res = database.com_pb_surrender_entry(self.data, self.work_data)
            if res == True:
                self.pb_surrender_top_level.destroy()
                self.on_close_pb_surrender_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.pb_surrender_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def pb_surrender_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.pb_surrender_update_scale_color(value)  # Update scale color based on value

    def convert_pb_surrender_app_no_to_uppercase(self):
        current_text = self.pb_surrender_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.pb_surrender_app_no_var.set(uppercase_text)


















    def open_np_surrender_win(self):
        if not self.np_surrender_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.np_surrender_top_level_open = True
            self.np_surrender_top_level = Toplevel()
            self.np_surrender_top_level.protocol("WM_DELETE_WINDOW", self.on_close_np_surrender_top_level)
            self.np_surrender_top_level.configure(bg='#B39CD0')
            screen_width = self.np_surrender_top_level.winfo_screenwidth()
            screen_height = self.np_surrender_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.np_surrender_top_level.title("NP SURRENDER")
            self.np_surrender_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.np_surrender_top_level.winfo_screenwidth()
            screen_height = self.np_surrender_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.np_surrender_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.np_surrender_top_level.resizable(False, False)
            self.np_surrender_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\np_surrender_bg.png"))
            Label(master=self.np_surrender_top_level,
                  image=self.np_surrender_bg_img).pack()

            self.np_surrender_time_lbl = Label(self.np_surrender_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.np_surrender_time_lbl.place(x=75,y=51)

            self.np_surrender_date_lbl = Label(self.np_surrender_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.np_surrender_date_lbl.place(x=195, y=51)

            self.np_surrender_combo_box = ttk.Combobox(self.np_surrender_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.np_surrender_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.np_surrender_scale = ttk.Scale(self.np_surrender_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.np_surrender_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.np_surrender_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["np_surrender_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.np_surrender_combo_box['values'] = self.combo_values

            self.np_surrender_combo_box.bind('<<ComboboxSelected>>', self.np_surrender_combo_fun)
            self.np_surrender_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.np_surrender_amount_var = StringVar()
            self.np_surrender_amount_entry = Entry(self.np_surrender_top_level,
                                                 textvariable=self.np_surrender_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.np_surrender_amount_entry.place(x=60, y=125)

            self.np_surrender_app_no_var = StringVar()
            self.np_surrender_app_no_entry = Entry(self.np_surrender_top_level,
                                         textvariable=self.np_surrender_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.np_surrender_app_no_entry.place(x=60, y=196)
            self.np_surrender_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_np_surrender_app_no_to_uppercase())

            self.np_surrender_status_var = StringVar()
            self.np_surrender_status_var.set("0")
            self.np_surrender_status_btn = Button(master=self.np_surrender_top_level,
                                                textvariable=self.np_surrender_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.np_surrender_status_change,
                                                borderwidth=0
                                                )
            self.np_surrender_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.np_surrender_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_np_surrender_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.np_surrender_top_level,image=self.delete_but_img,
                   command=self.np_surrender_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.np_surrender_top_level.mainloop()

    def on_close_np_surrender_top_level(self):
        self.np_surrender_top_level_open = False
        self.np_surrender_top_level.destroy()
        self.windows = "closed"

    def np_surrender_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def np_surrender_status_change(self):
        if self.np_surrender_status_var.get() == "0":
            self.np_surrender_status_btn.config(image=self.completed_status_img)
            self.np_surrender_status_var.set("1")
            print(self.np_surrender_status_var.get())
        elif self.np_surrender_status_var.get() == "1":
            self.np_surrender_status_btn.config(image=self.pending_status_img)
            self.np_surrender_status_var.set("0")
            print(self.np_surrender_status_var.get())

    def com_np_surrender_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.np_surrender_priority_var.get()))
        if self.np_surrender_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.np_surrender_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("np_surrender_amount") == None:
                print("1")
                if self.np_surrender_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["np_surrender_amount"] = self.np_surrender_amount_var.get()+","
                    self.data1["np_surrender_app_no"] = self.np_surrender_app_no_var.get()+","
                    self.data1["np_surrender_status"] = self.np_surrender_status_var.get()+","
                    self.data1["np_surrender_time"] = formatted_time + ","
                    self.data1["np_surrender_date"] = formatted_date + ","
                    self.data1["np_surrender_priority"] = self.con_value(round(self.np_surrender_scale.get()))+","





                    # adding np_surrender amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_surrender_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_np_surrender_entry(self.data, self.data1)
                    if res == True:
                        self.np_surrender_top_level.destroy()
                        self.on_close_np_surrender_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_surrender_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("np_surrender_amount") != None:
                print("2.0")
                if self.np_surrender_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["np_surrender_amount"] = self.work_data["np_surrender_amount"] +self.np_surrender_amount_var.get()+","
                    self.data1["np_surrender_app_no"] = self.work_data["np_surrender_app_no"] +self.np_surrender_app_no_var.get()+","
                    self.data1["np_surrender_status"] = self.work_data["np_surrender_status"] +self.np_surrender_status_var.get()+","
                    self.data1["np_surrender_time"] = self.work_data["np_surrender_time"] + formatted_time + ","
                    self.data1["np_surrender_date"] = self.work_data["np_surrender_date"] +formatted_date + ","
                    self.data1["np_surrender_priority"] = self.work_data["np_surrender_priority"] +self.con_value(round(self.np_surrender_scale.get()))+","




                    # adding np_surrender amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_surrender_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_np_surrender_entry(self.data, self.data1)
                    if res == True:
                        self.np_surrender_top_level.destroy()
                        self.on_close_np_surrender_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_surrender_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.np_surrender_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["np_surrender_amount"].split(',')
                    # removing old amount of np_surrender
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of np_surrender
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_surrender_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["np_surrender_amount"].split(',')
                    data[self.index] = self.np_surrender_amount_entry.get()
                    data =",".join(data)
                    self.work_data["np_surrender_amount"] = data

                    data = self.work_data["np_surrender_app_no"].split(',')
                    data[self.index] = self.np_surrender_app_no_var.get()
                    data =",".join(data)
                    self.work_data["np_surrender_app_no"] = data

                    data = self.work_data["np_surrender_status"].split(',')
                    data[self.index] = self.np_surrender_status_var.get()
                    data =",".join(data)
                    self.work_data["np_surrender_status"] = data

                    data = self.work_data["np_surrender_priority"].split(',')
                    data[self.index] = self.con_value(round(self.np_surrender_scale.get()))
                    data =",".join(data)
                    self.work_data["np_surrender_priority"] = data
                    # messagebox.showinfo(parent=self.np_surrender_top_level,title="",message=data)
                    res = database.com_np_surrender_entry(self.data, self.work_data)
                    if res == True:
                        self.np_surrender_top_level.destroy()
                        self.on_close_np_surrender_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.np_surrender_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def np_surrender_combo_fun(self, event):
        if self.np_surrender_combo_box.get() == "NEW ENTRY":
            self.np_surrender_amount_var.set("")
            self.np_surrender_app_no_var.set("")
            self.np_surrender_status_var.set("1")
            self.np_surrender_status_change()
            self.np_surrender_entry_selection_var = "NEW ENTRY"
            self.np_surrender_date_lbl.config(text="")
            self.np_surrender_time_lbl.config(text="")
            self.np_surrender_scale.set(0)


        # self.data[0]["np_surrender_amount"]
        else:
            self.np_surrender_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.np_surrender_combo_box.get())-1
            amount = self.work_data["np_surrender_amount"].split(",")
            app_no = self.work_data["np_surrender_app_no"].split(",")
            status = self.work_data["np_surrender_status"].split(",")
            date = self.work_data["np_surrender_date"].split(",")
            time = self.work_data["np_surrender_time"].split(",")
            priority = self.work_data["np_surrender_priority"].split(",")
            self.np_surrender_amount_var.set(amount[int(self.np_surrender_combo_box.get())-1])
            self.np_surrender_app_no_var.set(app_no[int(self.np_surrender_combo_box.get())-1])
            self.np_surrender_status_var.set(status[int(self.np_surrender_combo_box.get())-1])
            self.np_surrender_date_lbl.config(text=date[int(self.np_surrender_combo_box.get())-1])
            self.np_surrender_time_lbl.config(text=time[int(self.np_surrender_combo_box.get())-1])
            self.np_surrender_scale.set(self.con_value_rev(priority[int(self.np_surrender_combo_box.get())-1]))
            if self.np_surrender_status_var.get() == "0":
                self.np_surrender_status_btn.config(image=self.pending_status_img)
            elif self.np_surrender_status_var.get() == "1":
                self.np_surrender_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.np_surrender_top_level, title="",message="")

    def np_surrender_entry_delete_fun(self):
        if self.np_surrender_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["np_surrender_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["np_surrender_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_surrender_amount"] = data

            data = self.work_data["np_surrender_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_surrender_app_no"] = data

            data = self.work_data["np_surrender_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_surrender_status"] = data

            data = self.work_data["np_surrender_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_surrender_date"] = data

            data = self.work_data["np_surrender_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_surrender_time"] = data

            data = self.work_data["np_surrender_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_surrender_priority"] = data

            res = database.com_np_surrender_entry(self.data, self.work_data)
            if res == True:
                self.np_surrender_top_level.destroy()
                self.on_close_np_surrender_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.np_surrender_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def np_surrender_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.np_surrender_update_scale_color(value)  # Update scale color based on value

    def convert_np_surrender_app_no_to_uppercase(self):
        current_text = self.np_surrender_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.np_surrender_app_no_var.set(uppercase_text)



















    def open_pollution_win(self):
        if not self.pollution_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.pollution_top_level_open = True
            self.pollution_top_level = Toplevel()
            self.pollution_top_level.protocol("WM_DELETE_WINDOW", self.on_close_pollution_top_level)
            self.pollution_top_level.configure(bg='#B39CD0')
            screen_width = self.pollution_top_level.winfo_screenwidth()
            screen_height = self.pollution_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.pollution_top_level.title("POLLUTION")
            self.pollution_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.pollution_top_level.winfo_screenwidth()
            screen_height = self.pollution_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.pollution_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.pollution_top_level.resizable(False, False)
            self.pollution_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\pollution_bg.png"))
            Label(master=self.pollution_top_level,
                  image=self.pollution_bg_img).pack()

            self.pollution_time_lbl = Label(self.pollution_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.pollution_time_lbl.place(x=75,y=51)

            self.pollution_date_lbl = Label(self.pollution_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.pollution_date_lbl.place(x=195, y=51)

            self.pollution_combo_box = ttk.Combobox(self.pollution_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.pollution_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.pollution_scale = ttk.Scale(self.pollution_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.pollution_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.pollution_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["pollution_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.pollution_combo_box['values'] = self.combo_values

            self.pollution_combo_box.bind('<<ComboboxSelected>>', self.pollution_combo_fun)
            self.pollution_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.pollution_amount_var = StringVar()
            self.pollution_amount_entry = Entry(self.pollution_top_level,
                                                 textvariable=self.pollution_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.pollution_amount_entry.place(x=60, y=125)

            self.pollution_app_no_var = StringVar()
            self.pollution_app_no_entry = Entry(self.pollution_top_level,
                                         textvariable=self.pollution_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.pollution_app_no_entry.place(x=60, y=196)
            self.pollution_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_pollution_app_no_to_uppercase())

            self.pollution_status_var = StringVar()
            self.pollution_status_var.set("0")
            self.pollution_status_btn = Button(master=self.pollution_top_level,
                                                textvariable=self.pollution_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.pollution_status_change,
                                                borderwidth=0
                                                )
            self.pollution_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.pollution_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_pollution_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.pollution_top_level,image=self.delete_but_img,
                   command=self.pollution_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.pollution_top_level.mainloop()

    def on_close_pollution_top_level(self):
        self.pollution_top_level_open = False
        self.pollution_top_level.destroy()
        self.windows = "closed"

    def pollution_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def pollution_status_change(self):
        if self.pollution_status_var.get() == "0":
            self.pollution_status_btn.config(image=self.completed_status_img)
            self.pollution_status_var.set("1")
            print(self.pollution_status_var.get())
        elif self.pollution_status_var.get() == "1":
            self.pollution_status_btn.config(image=self.pending_status_img)
            self.pollution_status_var.set("0")
            print(self.pollution_status_var.get())

    def com_pollution_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.pollution_priority_var.get()))
        if self.pollution_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.pollution_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("pollution_amount") == None:
                print("1")
                if self.pollution_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["pollution_amount"] = self.pollution_amount_var.get()+","
                    self.data1["pollution_app_no"] = self.pollution_app_no_var.get()+","
                    self.data1["pollution_status"] = self.pollution_status_var.get()+","
                    self.data1["pollution_time"] = formatted_time + ","
                    self.data1["pollution_date"] = formatted_date + ","
                    self.data1["pollution_priority"] = self.con_value(round(self.pollution_scale.get()))+","





                    # adding pollution amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pollution_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_pollution_entry(self.data, self.data1)
                    if res == True:
                        self.pollution_top_level.destroy()
                        self.on_close_pollution_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pollution_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("pollution_amount") != None:
                print("2.0")
                if self.pollution_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["pollution_amount"] = self.work_data["pollution_amount"] +self.pollution_amount_var.get()+","
                    self.data1["pollution_app_no"] = self.work_data["pollution_app_no"] +self.pollution_app_no_var.get()+","
                    self.data1["pollution_status"] = self.work_data["pollution_status"] +self.pollution_status_var.get()+","
                    self.data1["pollution_time"] = self.work_data["pollution_time"] + formatted_time + ","
                    self.data1["pollution_date"] = self.work_data["pollution_date"] +formatted_date + ","
                    self.data1["pollution_priority"] = self.work_data["pollution_priority"] +self.con_value(round(self.pollution_scale.get()))+","




                    # adding pollution amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pollution_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_pollution_entry(self.data, self.data1)
                    if res == True:
                        self.pollution_top_level.destroy()
                        self.on_close_pollution_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pollution_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.pollution_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["pollution_amount"].split(',')
                    # removing old amount of pollution
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of pollution
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.pollution_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    data = self.work_data["pollution_amount"].split(',')
                    data[self.index] = self.pollution_amount_entry.get()
                    data =",".join(data)
                    self.work_data["pollution_amount"] = data

                    data = self.work_data["pollution_app_no"].split(',')
                    data[self.index] = self.pollution_app_no_var.get()
                    data =",".join(data)
                    self.work_data["pollution_app_no"] = data

                    data = self.work_data["pollution_status"].split(',')
                    data[self.index] = self.pollution_status_var.get()
                    data =",".join(data)
                    self.work_data["pollution_status"] = data

                    data = self.work_data["pollution_priority"].split(',')
                    data[self.index] = self.con_value(round(self.pollution_scale.get()))
                    data =",".join(data)
                    self.work_data["pollution_priority"] = data
                    # messagebox.showinfo(parent=self.pollution_top_level,title="",message=data)
                    res = database.com_pollution_entry(self.data, self.work_data)
                    if res == True:
                        self.pollution_top_level.destroy()
                        self.on_close_pollution_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.pollution_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def pollution_combo_fun(self, event):
        if self.pollution_combo_box.get() == "NEW ENTRY":
            self.pollution_amount_var.set("")
            self.pollution_app_no_var.set("")
            self.pollution_status_var.set("1")
            self.pollution_status_change()
            self.pollution_entry_selection_var = "NEW ENTRY"
            self.pollution_date_lbl.config(text="")
            self.pollution_time_lbl.config(text="")
            self.pollution_scale.set(0)


        # self.data[0]["pollution_amount"]
        else:
            self.pollution_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.pollution_combo_box.get())-1
            amount = self.work_data["pollution_amount"].split(",")
            app_no = self.work_data["pollution_app_no"].split(",")
            status = self.work_data["pollution_status"].split(",")
            date = self.work_data["pollution_date"].split(",")
            time = self.work_data["pollution_time"].split(",")
            priority = self.work_data["pollution_priority"].split(",")
            self.pollution_amount_var.set(amount[int(self.pollution_combo_box.get())-1])
            self.pollution_app_no_var.set(app_no[int(self.pollution_combo_box.get())-1])
            self.pollution_status_var.set(status[int(self.pollution_combo_box.get())-1])
            self.pollution_date_lbl.config(text=date[int(self.pollution_combo_box.get())-1])
            self.pollution_time_lbl.config(text=time[int(self.pollution_combo_box.get())-1])
            self.pollution_scale.set(self.con_value_rev(priority[int(self.pollution_combo_box.get())-1]))
            if self.pollution_status_var.get() == "0":
                self.pollution_status_btn.config(image=self.pending_status_img)
            elif self.pollution_status_var.get() == "1":
                self.pollution_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.pollution_top_level, title="",message="")

    def pollution_entry_delete_fun(self):
        if self.pollution_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)



            # these three line of code, subtract delete work amount from total
            data = self.work_data["pollution_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["pollution_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pollution_amount"] = data

            data = self.work_data["pollution_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pollution_app_no"] = data

            data = self.work_data["pollution_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pollution_status"] = data

            data = self.work_data["pollution_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pollution_date"] = data

            data = self.work_data["pollution_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pollution_time"] = data

            data = self.work_data["pollution_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["pollution_priority"] = data

            res = database.com_pollution_entry(self.data, self.work_data)
            if res == True:
                self.pollution_top_level.destroy()
                self.on_close_pollution_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.pollution_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def pollution_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.pollution_update_scale_color(value)  # Update scale color based on value

    def convert_pollution_app_no_to_uppercase(self):
        current_text = self.pollution_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.pollution_app_no_var.set(uppercase_text)



















    def open_address_change_win(self):
        if not self.address_change_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.address_change_top_level_open = True
            self.address_change_top_level = Toplevel()
            self.address_change_top_level.protocol("WM_DELETE_WINDOW", self.on_close_address_change_top_level)
            self.address_change_top_level.configure(bg='#B39CD0')
            screen_width = self.address_change_top_level.winfo_screenwidth()
            screen_height = self.address_change_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.address_change_top_level.title("ADDRESS CHANGE")
            self.address_change_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.address_change_top_level.winfo_screenwidth()
            screen_height = self.address_change_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.address_change_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.address_change_top_level.resizable(False, False)
            self.address_change_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\address_change_bg.png"))
            Label(master=self.address_change_top_level,
                  image=self.address_change_bg_img).pack()

            self.address_change_time_lbl = Label(self.address_change_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.address_change_time_lbl.place(x=75,y=51)

            self.address_change_date_lbl = Label(self.address_change_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.address_change_date_lbl.place(x=195, y=51)

            self.address_change_combo_box = ttk.Combobox(self.address_change_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.address_change_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.address_change_scale = ttk.Scale(self.address_change_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.address_change_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.address_change_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["address_change_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.address_change_combo_box['values'] = self.combo_values

            self.address_change_combo_box.bind('<<ComboboxSelected>>', self.address_change_combo_fun)
            self.address_change_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.address_change_amount_var = StringVar()
            self.address_change_amount_entry = Entry(self.address_change_top_level,
                                                 textvariable=self.address_change_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.address_change_amount_entry.place(x=60, y=125)

            self.address_change_app_no_var = StringVar()
            self.address_change_app_no_entry = Entry(self.address_change_top_level,
                                         textvariable=self.address_change_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.address_change_app_no_entry.place(x=60, y=196)
            self.address_change_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_address_change_app_no_to_uppercase())

            self.address_change_status_var = StringVar()
            self.address_change_status_var.set("0")
            self.address_change_status_btn = Button(master=self.address_change_top_level,
                                                textvariable=self.address_change_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.address_change_status_change,
                                                borderwidth=0
                                                )
            self.address_change_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.address_change_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_address_change_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.address_change_top_level,image=self.delete_but_img,
                   command=self.address_change_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.address_change_top_level.mainloop()

    def on_close_address_change_top_level(self):
        self.address_change_top_level_open = False
        self.address_change_top_level.destroy()
        self.windows = "closed"

    def address_change_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def address_change_status_change(self):
        if self.address_change_status_var.get() == "0":
            self.address_change_status_btn.config(image=self.completed_status_img)
            self.address_change_status_var.set("1")
            print(self.address_change_status_var.get())
        elif self.address_change_status_var.get() == "1":
            self.address_change_status_btn.config(image=self.pending_status_img)
            self.address_change_status_var.set("0")
            print(self.address_change_status_var.get())

    def com_address_change_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.address_change_priority_var.get()))
        if self.address_change_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.address_change_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("address_change_amount") == None:
                print("1")
                if self.address_change_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["address_change_amount"] = self.address_change_amount_var.get()+","
                    self.data1["address_change_app_no"] = self.address_change_app_no_var.get()+","
                    self.data1["address_change_status"] = self.address_change_status_var.get()+","
                    self.data1["address_change_time"] = formatted_time + ","
                    self.data1["address_change_date"] = formatted_date + ","
                    self.data1["address_change_priority"] = self.con_value(round(self.address_change_scale.get()))+","





                    # adding address_change amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.address_change_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_address_change_entry(self.data, self.data1)
                    if res == True:
                        self.address_change_top_level.destroy()
                        self.on_close_address_change_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.address_change_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("address_change_amount") != None:
                print("2.0")
                if self.address_change_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["address_change_amount"] = self.work_data["address_change_amount"] +self.address_change_amount_var.get()+","
                    self.data1["address_change_app_no"] = self.work_data["address_change_app_no"] +self.address_change_app_no_var.get()+","
                    self.data1["address_change_status"] = self.work_data["address_change_status"] +self.address_change_status_var.get()+","
                    self.data1["address_change_time"] = self.work_data["address_change_time"] + formatted_time + ","
                    self.data1["address_change_date"] = self.work_data["address_change_date"] +formatted_date + ","
                    self.data1["address_change_priority"] = self.work_data["address_change_priority"] +self.con_value(round(self.address_change_scale.get()))+","





                    # adding address_change amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.address_change_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_address_change_entry(self.data, self.data1)
                    if res == True:
                        self.address_change_top_level.destroy()
                        self.on_close_address_change_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.address_change_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.address_change_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["address_change_amount"].split(',')
                    # removing old amount of address_change
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of address_change
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.address_change_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["address_change_amount"].split(',')
                    data[self.index] = self.address_change_amount_entry.get()
                    data =",".join(data)
                    self.work_data["address_change_amount"] = data

                    data = self.work_data["address_change_app_no"].split(',')
                    data[self.index] = self.address_change_app_no_var.get()
                    data =",".join(data)
                    self.work_data["address_change_app_no"] = data

                    data = self.work_data["address_change_status"].split(',')
                    data[self.index] = self.address_change_status_var.get()
                    data =",".join(data)
                    self.work_data["address_change_status"] = data

                    data = self.work_data["address_change_priority"].split(',')
                    data[self.index] = self.con_value(round(self.address_change_scale.get()))
                    data =",".join(data)
                    self.work_data["address_change_priority"] = data
                    # messagebox.showinfo(parent=self.address_change_top_level,title="",message=data)
                    res = database.com_address_change_entry(self.data, self.work_data)
                    if res == True:
                        self.address_change_top_level.destroy()
                        self.on_close_address_change_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.address_change_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def address_change_combo_fun(self, event):
        if self.address_change_combo_box.get() == "NEW ENTRY":
            self.address_change_amount_var.set("")
            self.address_change_app_no_var.set("")
            self.address_change_status_var.set("1")
            self.address_change_status_change()
            self.address_change_entry_selection_var = "NEW ENTRY"
            self.address_change_date_lbl.config(text="")
            self.address_change_time_lbl.config(text="")
            self.address_change_scale.set(0)


        # self.data[0]["address_change_amount"]
        else:
            self.address_change_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.address_change_combo_box.get())-1
            amount = self.work_data["address_change_amount"].split(",")
            app_no = self.work_data["address_change_app_no"].split(",")
            status = self.work_data["address_change_status"].split(",")
            date = self.work_data["address_change_date"].split(",")
            time = self.work_data["address_change_time"].split(",")
            priority = self.work_data["address_change_priority"].split(",")
            self.address_change_amount_var.set(amount[int(self.address_change_combo_box.get())-1])
            self.address_change_app_no_var.set(app_no[int(self.address_change_combo_box.get())-1])
            self.address_change_status_var.set(status[int(self.address_change_combo_box.get())-1])
            self.address_change_date_lbl.config(text=date[int(self.address_change_combo_box.get())-1])
            self.address_change_time_lbl.config(text=time[int(self.address_change_combo_box.get())-1])
            self.address_change_scale.set(self.con_value_rev(priority[int(self.address_change_combo_box.get())-1]))
            if self.address_change_status_var.get() == "0":
                self.address_change_status_btn.config(image=self.pending_status_img)
            elif self.address_change_status_var.get() == "1":
                self.address_change_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.address_change_top_level, title="",message="")

    def address_change_entry_delete_fun(self):
        if self.address_change_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["address_change_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])





            data = self.work_data["address_change_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["address_change_amount"] = data

            data = self.work_data["address_change_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["address_change_app_no"] = data

            data = self.work_data["address_change_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["address_change_status"] = data

            data = self.work_data["address_change_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["address_change_date"] = data

            data = self.work_data["address_change_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["address_change_time"] = data

            data = self.work_data["address_change_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["address_change_priority"] = data

            res = database.com_address_change_entry(self.data, self.work_data)
            if res == True:
                self.address_change_top_level.destroy()
                self.on_close_address_change_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.address_change_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def address_change_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.address_change_update_scale_color(value)  # Update scale color based on value

    def convert_address_change_app_no_to_uppercase(self):
        current_text = self.address_change_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.address_change_app_no_var.set(uppercase_text)


















    def open_fancy_number_win(self):
        if not self.fancy_number_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.fancy_number_top_level_open = True
            self.fancy_number_top_level = Toplevel()
            self.fancy_number_top_level.protocol("WM_DELETE_WINDOW", self.on_close_fancy_number_top_level)
            self.fancy_number_top_level.configure(bg='#B39CD0')
            screen_width = self.fancy_number_top_level.winfo_screenwidth()
            screen_height = self.fancy_number_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.fancy_number_top_level.title("FANCY NUMBER")
            self.fancy_number_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.fancy_number_top_level.winfo_screenwidth()
            screen_height = self.fancy_number_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.fancy_number_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.fancy_number_top_level.resizable(False, False)
            self.fancy_number_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\fancy_number_bg.png"))
            Label(master=self.fancy_number_top_level,
                  image=self.fancy_number_bg_img).pack()

            self.fancy_number_time_lbl = Label(self.fancy_number_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.fancy_number_time_lbl.place(x=75,y=51)

            self.fancy_number_date_lbl = Label(self.fancy_number_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.fancy_number_date_lbl.place(x=195, y=51)

            self.fancy_number_combo_box = ttk.Combobox(self.fancy_number_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.fancy_number_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.fancy_number_scale = ttk.Scale(self.fancy_number_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.fancy_number_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.fancy_number_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["fancy_number_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.fancy_number_combo_box['values'] = self.combo_values

            self.fancy_number_combo_box.bind('<<ComboboxSelected>>', self.fancy_number_combo_fun)
            self.fancy_number_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.fancy_number_amount_var = StringVar()
            self.fancy_number_amount_entry = Entry(self.fancy_number_top_level,
                                                 textvariable=self.fancy_number_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.fancy_number_amount_entry.place(x=60, y=125)

            self.fancy_number_app_no_var = StringVar()
            self.fancy_number_app_no_entry = Entry(self.fancy_number_top_level,
                                         textvariable=self.fancy_number_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.fancy_number_app_no_entry.place(x=60, y=196)
            self.fancy_number_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_fancy_number_app_no_to_uppercase())

            self.fancy_number_status_var = StringVar()
            self.fancy_number_status_var.set("0")
            self.fancy_number_status_btn = Button(master=self.fancy_number_top_level,
                                                textvariable=self.fancy_number_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.fancy_number_status_change,
                                                borderwidth=0
                                                )
            self.fancy_number_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.fancy_number_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_fancy_number_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.fancy_number_top_level,image=self.delete_but_img,
                   command=self.fancy_number_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.fancy_number_top_level.mainloop()

    def on_close_fancy_number_top_level(self):
        self.fancy_number_top_level_open = False
        self.fancy_number_top_level.destroy()
        self.windows = "closed"

    def fancy_number_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def fancy_number_status_change(self):
        if self.fancy_number_status_var.get() == "0":
            self.fancy_number_status_btn.config(image=self.completed_status_img)
            self.fancy_number_status_var.set("1")
            print(self.fancy_number_status_var.get())
        elif self.fancy_number_status_var.get() == "1":
            self.fancy_number_status_btn.config(image=self.pending_status_img)
            self.fancy_number_status_var.set("0")
            print(self.fancy_number_status_var.get())

    def com_fancy_number_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.fancy_number_priority_var.get()))
        if self.fancy_number_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.fancy_number_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("fancy_number_amount") == None:
                print("1")
                if self.fancy_number_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["fancy_number_amount"] = self.fancy_number_amount_var.get()+","
                    self.data1["fancy_number_app_no"] = self.fancy_number_app_no_var.get()+","
                    self.data1["fancy_number_status"] = self.fancy_number_status_var.get()+","
                    self.data1["fancy_number_time"] = formatted_time + ","
                    self.data1["fancy_number_date"] = formatted_date + ","
                    self.data1["fancy_number_priority"] = self.con_value(round(self.fancy_number_scale.get()))+","





                    # adding fancy_number amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.fancy_number_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    res = database.com_fancy_number_entry(self.data, self.data1)
                    if res == True:
                        self.fancy_number_top_level.destroy()
                        self.on_close_fancy_number_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.fancy_number_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("fancy_number_amount") != None:
                print("2.0")
                if self.fancy_number_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["fancy_number_amount"] = self.work_data["fancy_number_amount"] +self.fancy_number_amount_var.get()+","
                    self.data1["fancy_number_app_no"] = self.work_data["fancy_number_app_no"] +self.fancy_number_app_no_var.get()+","
                    self.data1["fancy_number_status"] = self.work_data["fancy_number_status"] +self.fancy_number_status_var.get()+","
                    self.data1["fancy_number_time"] = self.work_data["fancy_number_time"] + formatted_time + ","
                    self.data1["fancy_number_date"] = self.work_data["fancy_number_date"] +formatted_date + ","
                    self.data1["fancy_number_priority"] = self.work_data["fancy_number_priority"] +self.con_value(round(self.fancy_number_scale.get()))+","




                    # adding fancy_number amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.fancy_number_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_fancy_number_entry(self.data, self.data1)
                    if res == True:
                        self.fancy_number_top_level.destroy()
                        self.on_close_fancy_number_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.fancy_number_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.fancy_number_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")





                    data = self.work_data["fancy_number_amount"].split(',')
                    # removing old amount of fancy_number
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of fancy_number
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.fancy_number_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["fancy_number_amount"].split(',')
                    data[self.index] = self.fancy_number_amount_entry.get()
                    data =",".join(data)
                    self.work_data["fancy_number_amount"] = data

                    data = self.work_data["fancy_number_app_no"].split(',')
                    data[self.index] = self.fancy_number_app_no_var.get()
                    data =",".join(data)
                    self.work_data["fancy_number_app_no"] = data

                    data = self.work_data["fancy_number_status"].split(',')
                    data[self.index] = self.fancy_number_status_var.get()
                    data =",".join(data)
                    self.work_data["fancy_number_status"] = data

                    data = self.work_data["fancy_number_priority"].split(',')
                    data[self.index] = self.con_value(round(self.fancy_number_scale.get()))
                    data =",".join(data)
                    self.work_data["fancy_number_priority"] = data
                    # messagebox.showinfo(parent=self.fancy_number_top_level,title="",message=data)
                    res = database.com_fancy_number_entry(self.data, self.work_data)
                    if res == True:
                        self.fancy_number_top_level.destroy()
                        self.on_close_fancy_number_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.fancy_number_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def fancy_number_combo_fun(self, event):
        if self.fancy_number_combo_box.get() == "NEW ENTRY":
            self.fancy_number_amount_var.set("")
            self.fancy_number_app_no_var.set("")
            self.fancy_number_status_var.set("1")
            self.fancy_number_status_change()
            self.fancy_number_entry_selection_var = "NEW ENTRY"
            self.fancy_number_date_lbl.config(text="")
            self.fancy_number_time_lbl.config(text="")
            self.fancy_number_scale.set(0)


        # self.data[0]["fancy_number_amount"]
        else:
            self.fancy_number_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.fancy_number_combo_box.get())-1
            amount = self.work_data["fancy_number_amount"].split(",")
            app_no = self.work_data["fancy_number_app_no"].split(",")
            status = self.work_data["fancy_number_status"].split(",")
            date = self.work_data["fancy_number_date"].split(",")
            time = self.work_data["fancy_number_time"].split(",")
            priority = self.work_data["fancy_number_priority"].split(",")
            self.fancy_number_amount_var.set(amount[int(self.fancy_number_combo_box.get())-1])
            self.fancy_number_app_no_var.set(app_no[int(self.fancy_number_combo_box.get())-1])
            self.fancy_number_status_var.set(status[int(self.fancy_number_combo_box.get())-1])
            self.fancy_number_date_lbl.config(text=date[int(self.fancy_number_combo_box.get())-1])
            self.fancy_number_time_lbl.config(text=time[int(self.fancy_number_combo_box.get())-1])
            self.fancy_number_scale.set(self.con_value_rev(priority[int(self.fancy_number_combo_box.get())-1]))
            if self.fancy_number_status_var.get() == "0":
                self.fancy_number_status_btn.config(image=self.pending_status_img)
            elif self.fancy_number_status_var.get() == "1":
                self.fancy_number_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.fancy_number_top_level, title="",message="")

    def fancy_number_entry_delete_fun(self):
        if self.fancy_number_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)




            # these three line of code, subtract delete work amount from total
            data = self.work_data["fancy_number_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["fancy_number_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fancy_number_amount"] = data

            data = self.work_data["fancy_number_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fancy_number_app_no"] = data

            data = self.work_data["fancy_number_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fancy_number_status"] = data

            data = self.work_data["fancy_number_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fancy_number_date"] = data

            data = self.work_data["fancy_number_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fancy_number_time"] = data

            data = self.work_data["fancy_number_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["fancy_number_priority"] = data

            res = database.com_fancy_number_entry(self.data, self.work_data)
            if res == True:
                self.fancy_number_top_level.destroy()
                self.on_close_fancy_number_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.fancy_number_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def fancy_number_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.fancy_number_update_scale_color(value)  # Update scale color based on value

    def convert_fancy_number_app_no_to_uppercase(self):
        current_text = self.fancy_number_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.fancy_number_app_no_var.set(uppercase_text)





















    def open_phone_change_win(self):
        if not self.phone_change_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.phone_change_top_level_open = True
            self.phone_change_top_level = Toplevel()
            self.phone_change_top_level.protocol("WM_DELETE_WINDOW", self.on_close_phone_change_top_level)
            self.phone_change_top_level.configure(bg='#B39CD0')
            screen_width = self.phone_change_top_level.winfo_screenwidth()
            screen_height = self.phone_change_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.phone_change_top_level.title("PHONE CHANGE")
            self.phone_change_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.phone_change_top_level.winfo_screenwidth()
            screen_height = self.phone_change_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.phone_change_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.phone_change_top_level.resizable(False, False)
            self.phone_change_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\phone_change_bg.png"))
            Label(master=self.phone_change_top_level,
                  image=self.phone_change_bg_img).pack()

            self.phone_change_time_lbl = Label(self.phone_change_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.phone_change_time_lbl.place(x=75,y=51)

            self.phone_change_date_lbl = Label(self.phone_change_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.phone_change_date_lbl.place(x=195, y=51)

            self.phone_change_combo_box = ttk.Combobox(self.phone_change_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.phone_change_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.phone_change_scale = ttk.Scale(self.phone_change_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.phone_change_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.phone_change_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["phone_change_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.phone_change_combo_box['values'] = self.combo_values

            self.phone_change_combo_box.bind('<<ComboboxSelected>>', self.phone_change_combo_fun)
            self.phone_change_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.phone_change_amount_var = StringVar()
            self.phone_change_amount_entry = Entry(self.phone_change_top_level,
                                                 textvariable=self.phone_change_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.phone_change_amount_entry.place(x=60, y=125)

            self.phone_change_app_no_var = StringVar()
            self.phone_change_app_no_entry = Entry(self.phone_change_top_level,
                                         textvariable=self.phone_change_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.phone_change_app_no_entry.place(x=60, y=196)
            self.phone_change_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_phone_change_app_no_to_uppercase())

            self.phone_change_status_var = StringVar()
            self.phone_change_status_var.set("0")
            self.phone_change_status_btn = Button(master=self.phone_change_top_level,
                                                textvariable=self.phone_change_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.phone_change_status_change,
                                                borderwidth=0
                                                )
            self.phone_change_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.phone_change_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_phone_change_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.phone_change_top_level,image=self.delete_but_img,
                   command=self.phone_change_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.phone_change_top_level.mainloop()

    def on_close_phone_change_top_level(self):
        self.phone_change_top_level_open = False
        self.phone_change_top_level.destroy()
        self.windows = "closed"

    def phone_change_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def phone_change_status_change(self):
        if self.phone_change_status_var.get() == "0":
            self.phone_change_status_btn.config(image=self.completed_status_img)
            self.phone_change_status_var.set("1")
            print(self.phone_change_status_var.get())
        elif self.phone_change_status_var.get() == "1":
            self.phone_change_status_btn.config(image=self.pending_status_img)
            self.phone_change_status_var.set("0")
            print(self.phone_change_status_var.get())

    def com_phone_change_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.phone_change_priority_var.get()))
        if self.phone_change_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.phone_change_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("phone_change_amount") == None:
                print("1")
                if self.phone_change_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["phone_change_amount"] = self.phone_change_amount_var.get()+","
                    self.data1["phone_change_app_no"] = self.phone_change_app_no_var.get()+","
                    self.data1["phone_change_status"] = self.phone_change_status_var.get()+","
                    self.data1["phone_change_time"] = formatted_time + ","
                    self.data1["phone_change_date"] = formatted_date + ","
                    self.data1["phone_change_priority"] = self.con_value(round(self.phone_change_scale.get()))+","





                    # adding phone_change amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.phone_change_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_phone_change_entry(self.data, self.data1)
                    if res == True:
                        self.phone_change_top_level.destroy()
                        self.on_close_phone_change_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.phone_change_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("phone_change_amount") != None:
                print("2.0")
                if self.phone_change_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["phone_change_amount"] = self.work_data["phone_change_amount"] +self.phone_change_amount_var.get()+","
                    self.data1["phone_change_app_no"] = self.work_data["phone_change_app_no"] +self.phone_change_app_no_var.get()+","
                    self.data1["phone_change_status"] = self.work_data["phone_change_status"] +self.phone_change_status_var.get()+","
                    self.data1["phone_change_time"] = self.work_data["phone_change_time"] + formatted_time + ","
                    self.data1["phone_change_date"] = self.work_data["phone_change_date"] +formatted_date + ","
                    self.data1["phone_change_priority"] = self.work_data["phone_change_priority"] +self.con_value(round(self.phone_change_scale.get()))+","




                    # adding phone_change amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.phone_change_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])






                    res = database.com_phone_change_entry(self.data, self.data1)
                    if res == True:
                        self.phone_change_top_level.destroy()
                        self.on_close_phone_change_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.phone_change_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.phone_change_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")





                    data = self.work_data["phone_change_amount"].split(',')
                    # removing old amount of phone_change
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of phone_change
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.phone_change_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["phone_change_amount"].split(',')
                    data[self.index] = self.phone_change_amount_entry.get()
                    data =",".join(data)
                    self.work_data["phone_change_amount"] = data

                    data = self.work_data["phone_change_app_no"].split(',')
                    data[self.index] = self.phone_change_app_no_var.get()
                    data =",".join(data)
                    self.work_data["phone_change_app_no"] = data

                    data = self.work_data["phone_change_status"].split(',')
                    data[self.index] = self.phone_change_status_var.get()
                    data =",".join(data)
                    self.work_data["phone_change_status"] = data

                    data = self.work_data["phone_change_priority"].split(',')
                    data[self.index] = self.con_value(round(self.phone_change_scale.get()))
                    data =",".join(data)
                    self.work_data["phone_change_priority"] = data
                    # messagebox.showinfo(parent=self.phone_change_top_level,title="",message=data)
                    res = database.com_phone_change_entry(self.data, self.work_data)
                    if res == True:
                        self.phone_change_top_level.destroy()
                        self.on_close_phone_change_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.phone_change_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def phone_change_combo_fun(self, event):
        if self.phone_change_combo_box.get() == "NEW ENTRY":
            self.phone_change_amount_var.set("")
            self.phone_change_app_no_var.set("")
            self.phone_change_status_var.set("1")
            self.phone_change_status_change()
            self.phone_change_entry_selection_var = "NEW ENTRY"
            self.phone_change_date_lbl.config(text="")
            self.phone_change_time_lbl.config(text="")
            self.phone_change_scale.set(0)


        # self.data[0]["phone_change_amount"]
        else:
            self.phone_change_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.phone_change_combo_box.get())-1
            amount = self.work_data["phone_change_amount"].split(",")
            app_no = self.work_data["phone_change_app_no"].split(",")
            status = self.work_data["phone_change_status"].split(",")
            date = self.work_data["phone_change_date"].split(",")
            time = self.work_data["phone_change_time"].split(",")
            priority = self.work_data["phone_change_priority"].split(",")
            self.phone_change_amount_var.set(amount[int(self.phone_change_combo_box.get())-1])
            self.phone_change_app_no_var.set(app_no[int(self.phone_change_combo_box.get())-1])
            self.phone_change_status_var.set(status[int(self.phone_change_combo_box.get())-1])
            self.phone_change_date_lbl.config(text=date[int(self.phone_change_combo_box.get())-1])
            self.phone_change_time_lbl.config(text=time[int(self.phone_change_combo_box.get())-1])
            self.phone_change_scale.set(self.con_value_rev(priority[int(self.phone_change_combo_box.get())-1]))
            if self.phone_change_status_var.get() == "0":
                self.phone_change_status_btn.config(image=self.pending_status_img)
            elif self.phone_change_status_var.get() == "1":
                self.phone_change_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.phone_change_top_level, title="",message="")

    def phone_change_entry_delete_fun(self):
        if self.phone_change_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)





            # these three line of code, subtract delete work amount from total
            data = self.work_data["phone_change_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])






            data = self.work_data["phone_change_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["phone_change_amount"] = data

            data = self.work_data["phone_change_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["phone_change_app_no"] = data

            data = self.work_data["phone_change_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["phone_change_status"] = data

            data = self.work_data["phone_change_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["phone_change_date"] = data

            data = self.work_data["phone_change_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["phone_change_time"] = data

            data = self.work_data["phone_change_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["phone_change_priority"] = data

            res = database.com_phone_change_entry(self.data, self.work_data)
            if res == True:
                self.phone_change_top_level.destroy()
                self.on_close_phone_change_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.phone_change_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def phone_change_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.phone_change_update_scale_color(value)  # Update scale color based on value

    def convert_phone_change_app_no_to_uppercase(self):
        current_text = self.phone_change_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.phone_change_app_no_var.set(uppercase_text)



















    def open_np_authorization_win(self):
        if not self.np_authorization_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.np_authorization_top_level_open = True
            self.np_authorization_top_level = Toplevel()
            self.np_authorization_top_level.protocol("WM_DELETE_WINDOW", self.on_close_np_authorization_top_level)
            self.np_authorization_top_level.configure(bg='#B39CD0')
            screen_width = self.np_authorization_top_level.winfo_screenwidth()
            screen_height = self.np_authorization_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.np_authorization_top_level.title("NP AUTHORIZATION")
            self.np_authorization_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.np_authorization_top_level.winfo_screenwidth()
            screen_height = self.np_authorization_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.np_authorization_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.np_authorization_top_level.resizable(False, False)
            self.np_authorization_bg_img = ImageTk.PhotoImage(
                Image.open(r"images\all_work_img\np_authorization_bg.png"))
            Label(master=self.np_authorization_top_level,
                  image=self.np_authorization_bg_img).pack()

            self.np_authorization_time_lbl = Label(self.np_authorization_top_level, bg="#3b0085",
                                                   foreground="white", text="",
                                                   font=("helvatica", self.label_size, "bold"))
            self.np_authorization_time_lbl.place(x=75, y=51)

            self.np_authorization_date_lbl = Label(self.np_authorization_top_level, bg="#3b0085",
                                                   foreground="white", text="",
                                                   font=("helvatica", self.label_size, "bold"))
            self.np_authorization_date_lbl.place(x=195, y=51)

            self.np_authorization_combo_box = ttk.Combobox(self.np_authorization_top_level,
                                                           font=("helvatica", self.combobox_size, "bold"),
                                                           width=self.combobox_width,
                                                           state="readonly")
            self.np_authorization_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc",
                                 sliderthickness=10,
                                 sliderlength=50)
            # Create a Scale widget using ttk
            self.np_authorization_scale = ttk.Scale(self.np_authorization_top_level, from_=0, to=2, orient=HORIZONTAL,
                                                    command=self.np_authorization_on_scale_change,
                                                    style="Custom.Horizontal.TScale")
            self.np_authorization_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

            self.combo_values = ["NEW ENTRY", ]
            try:
                data = self.work_data["np_authorization_amount"]
                split_data = data.split(',')
                self.combo_values += [i + 1 for i in range(len(split_data) - 1)]
            except:
                pass
            self.np_authorization_combo_box['values'] = self.combo_values

            self.np_authorization_combo_box.bind('<<ComboboxSelected>>', self.np_authorization_combo_fun)
            self.np_authorization_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.np_authorization_amount_var = StringVar()
            self.np_authorization_amount_entry = Entry(self.np_authorization_top_level,
                                                       textvariable=self.np_authorization_amount_var,
                                                       bg=self.color_1,
                                                       # disabledbackground=self.color_1,
                                                       validate="key",
                                                       validatecommand=(self.main_root.register(self.validate_amount),
                                                                        "%S"),
                                                       border=0,
                                                       width=self.field_width_2,
                                                       font=("Helvetica", self.font_size))
            self.np_authorization_amount_entry.place(x=60, y=125)

            self.np_authorization_app_no_var = StringVar()
            self.np_authorization_app_no_entry = Entry(self.np_authorization_top_level,
                                                       textvariable=self.np_authorization_app_no_var,
                                                       validate="key",
                                                       validatecommand=(
                                                       self.main_root.register(self.validate_data), "%P"),
                                                       width=self.field_width_2,
                                                       bg=self.color_1,
                                                       border=0,
                                                       font=("Helvetica", self.font_size))
            self.np_authorization_app_no_entry.place(x=60, y=196)
            self.np_authorization_app_no_entry.bind('<KeyRelease>',
                                                    lambda event: self.convert_np_authorization_app_no_to_uppercase())

            self.np_authorization_status_var = StringVar()
            self.np_authorization_status_var.set("0")
            self.np_authorization_status_btn = Button(master=self.np_authorization_top_level,
                                                      textvariable=self.np_authorization_status_var,
                                                      image=self.pending_status_img,
                                                      bg=self.bg_color,
                                                      activebackground=self.bg_color,
                                                      command=self.np_authorization_status_change,
                                                      borderwidth=0
                                                      )
            self.np_authorization_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.np_authorization_top_level, text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_np_authorization_entry_fun).place(x=150, y=420)

            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.np_authorization_top_level, image=self.delete_but_img,
                   command=self.np_authorization_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)

            self.np_authorization_top_level.mainloop()

    def on_close_np_authorization_top_level(self):
        self.np_authorization_top_level_open = False
        self.np_authorization_top_level.destroy()
        self.windows = "closed"

    def np_authorization_update_scale_color(self, value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                           background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                           troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def np_authorization_status_change(self):
        if self.np_authorization_status_var.get() == "0":
            self.np_authorization_status_btn.config(image=self.completed_status_img)
            self.np_authorization_status_var.set("1")
            print(self.np_authorization_status_var.get())
        elif self.np_authorization_status_var.get() == "1":
            self.np_authorization_status_btn.config(image=self.pending_status_img)
            self.np_authorization_status_var.set("0")
            print(self.np_authorization_status_var.get())

    def com_np_authorization_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.np_authorization_priority_var.get()))
        if self.np_authorization_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field", message="Please Enter Amount",
                                   parent=self.np_authorization_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("np_authorization_amount") == None:
                print("1")
                if self.np_authorization_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["np_authorization_amount"] = self.np_authorization_amount_var.get() + ","
                    self.data1["np_authorization_app_no"] = self.np_authorization_app_no_var.get() + ","
                    self.data1["np_authorization_status"] = self.np_authorization_status_var.get() + ","
                    self.data1["np_authorization_time"] = formatted_time + ","
                    self.data1["np_authorization_date"] = formatted_date + ","
                    self.data1["np_authorization_priority"] = self.con_value(round(self.np_authorization_scale.get())) + ","




                    # adding np_authorization amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_authorization_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_np_authorization_entry(self.data, self.data1)
                    if res == True:
                        self.np_authorization_top_level.destroy()
                        self.on_close_np_authorization_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                             parent=self.np_authorization_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
            elif self.data1.get("np_authorization_amount") != None:
                print("2.0")
                if self.np_authorization_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["np_authorization_amount"] = self.work_data[
                                                                  "np_authorization_amount"] + self.np_authorization_amount_var.get() + ","
                    self.data1["np_authorization_app_no"] = self.work_data[
                                                                  "np_authorization_app_no"] + self.np_authorization_app_no_var.get() + ","
                    self.data1["np_authorization_status"] = self.work_data[
                                                                  "np_authorization_status"] + self.np_authorization_status_var.get() + ","
                    self.data1["np_authorization_time"] = self.work_data["np_authorization_time"] + formatted_time + ","
                    self.data1["np_authorization_date"] = self.work_data["np_authorization_date"] + formatted_date + ","
                    self.data1["np_authorization_priority"] = self.work_data["np_authorization_priority"] + self.con_value(
                        round(self.np_authorization_scale.get())) + ","




                    # adding np_authorization amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_authorization_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])





                    res = database.com_np_authorization_entry(self.data, self.data1)
                    if res == True:
                        self.np_authorization_top_level.destroy()
                        self.on_close_np_authorization_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                             parent=self.np_authorization_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.np_authorization_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")




                    data = self.work_data["np_authorization_amount"].split(',')
                    # removing old amount of np_authorization
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of np_authorization
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.np_authorization_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])




                    data = self.work_data["np_authorization_amount"].split(',')
                    data[self.index] = self.np_authorization_amount_entry.get()
                    data = ",".join(data)
                    self.work_data["np_authorization_amount"] = data

                    data = self.work_data["np_authorization_app_no"].split(',')
                    data[self.index] = self.np_authorization_app_no_var.get()
                    data = ",".join(data)
                    self.work_data["np_authorization_app_no"] = data

                    data = self.work_data["np_authorization_status"].split(',')
                    data[self.index] = self.np_authorization_status_var.get()
                    data = ",".join(data)
                    self.work_data["np_authorization_status"] = data

                    data = self.work_data["np_authorization_priority"].split(',')
                    data[self.index] = self.con_value(round(self.np_authorization_scale.get()))
                    data = ",".join(data)
                    self.work_data["np_authorization_priority"] = data
                    # messagebox.showinfo(parent=self.np_authorization_top_level,title="",message=data)
                    res = database.com_np_authorization_entry(self.data, self.work_data)
                    if res == True:
                        self.np_authorization_top_level.destroy()
                        self.on_close_np_authorization_top_level()
                        self.update_data(self.all_data, self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                             parent=self.np_authorization_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def np_authorization_combo_fun(self, event):
        if self.np_authorization_combo_box.get() == "NEW ENTRY":
            self.np_authorization_amount_var.set("")
            self.np_authorization_app_no_var.set("")
            self.np_authorization_status_var.set("1")
            self.np_authorization_status_change()
            self.np_authorization_entry_selection_var = "NEW ENTRY"
            self.np_authorization_date_lbl.config(text="")
            self.np_authorization_time_lbl.config(text="")
            self.np_authorization_scale.set(0)


        # self.data[0]["np_authorization_amount"]
        else:
            self.np_authorization_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.np_authorization_combo_box.get()) - 1
            amount = self.work_data["np_authorization_amount"].split(",")
            app_no = self.work_data["np_authorization_app_no"].split(",")
            status = self.work_data["np_authorization_status"].split(",")
            date = self.work_data["np_authorization_date"].split(",")
            time = self.work_data["np_authorization_time"].split(",")
            priority = self.work_data["np_authorization_priority"].split(",")
            self.np_authorization_amount_var.set(amount[int(self.np_authorization_combo_box.get()) - 1])
            self.np_authorization_app_no_var.set(app_no[int(self.np_authorization_combo_box.get()) - 1])
            self.np_authorization_status_var.set(status[int(self.np_authorization_combo_box.get()) - 1])
            self.np_authorization_date_lbl.config(text=date[int(self.np_authorization_combo_box.get()) - 1])
            self.np_authorization_time_lbl.config(text=time[int(self.np_authorization_combo_box.get()) - 1])
            self.np_authorization_scale.set(self.con_value_rev(priority[int(self.np_authorization_combo_box.get()) - 1]))
            if self.np_authorization_status_var.get() == "0":
                self.np_authorization_status_btn.config(image=self.pending_status_img)
            elif self.np_authorization_status_var.get() == "1":
                self.np_authorization_status_btn.config(image=self.completed_status_img)
        # pass
        # messagebox.showinfo(parent=self.np_authorization_top_level, title="",message="")

    def np_authorization_entry_delete_fun(self):
        if self.np_authorization_combo_box.get().isdigit():  # condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)



            # these three line of code, subtract delete work amount from total
            data = self.work_data["np_authorization_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])




            data = self.work_data["np_authorization_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_authorization_amount"] = data

            data = self.work_data["np_authorization_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_authorization_app_no"] = data

            data = self.work_data["np_authorization_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_authorization_status"] = data

            data = self.work_data["np_authorization_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_authorization_date"] = data

            data = self.work_data["np_authorization_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_authorization_time"] = data

            data = self.work_data["np_authorization_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["np_authorization_priority"] = data

            res = database.com_np_authorization_entry(self.data, self.work_data)
            if res == True:
                self.np_authorization_top_level.destroy()
                self.on_close_np_authorization_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.np_authorization_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def np_authorization_on_scale_change(self, value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.np_authorization_update_scale_color(value)  # Update scale color based on value

    def convert_np_authorization_app_no_to_uppercase(self):
        current_text = self.np_authorization_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.np_authorization_app_no_var.set(uppercase_text)



















    def open_rc_new_win(self):
        if not self.rc_new_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.rc_new_top_level_open = True
            self.rc_new_top_level = Toplevel()
            self.rc_new_top_level.protocol("WM_DELETE_WINDOW", self.on_close_rc_new_top_level)
            self.rc_new_top_level.configure(bg='#B39CD0')
            screen_width = self.rc_new_top_level.winfo_screenwidth()
            screen_height = self.rc_new_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.rc_new_top_level.title("RC NEW")
            self.rc_new_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.rc_new_top_level.winfo_screenwidth()
            screen_height = self.rc_new_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.rc_new_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.rc_new_top_level.resizable(False, False)
            self.rc_new_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_new_bg.png"))
            Label(master=self.rc_new_top_level,
                  image=self.rc_new_bg_img).pack()

            self.rc_new_time_lbl = Label(self.rc_new_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.rc_new_time_lbl.place(x=75,y=51)

            self.rc_new_date_lbl = Label(self.rc_new_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.rc_new_date_lbl.place(x=195, y=51)

            self.rc_new_combo_box = ttk.Combobox(self.rc_new_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.rc_new_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.rc_new_scale = ttk.Scale(self.rc_new_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.rc_new_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.rc_new_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["rc_new_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.rc_new_combo_box['values'] = self.combo_values

            self.rc_new_combo_box.bind('<<ComboboxSelected>>', self.rc_new_combo_fun)
            self.rc_new_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.rc_new_amount_var = StringVar()
            self.rc_new_amount_entry = Entry(self.rc_new_top_level,
                                                 textvariable=self.rc_new_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.rc_new_amount_entry.place(x=60, y=125)

            self.rc_new_app_no_var = StringVar()
            self.rc_new_app_no_entry = Entry(self.rc_new_top_level,
                                         textvariable=self.rc_new_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.rc_new_app_no_entry.place(x=60, y=196)
            self.rc_new_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_rc_new_app_no_to_uppercase())


            self.rc_new_status_var = StringVar()
            self.rc_new_status_var.set("0")
            self.rc_new_status_btn = Button(master=self.rc_new_top_level,
                                                textvariable=self.rc_new_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.rc_new_status_change,
                                                borderwidth=0
                                                )
            self.rc_new_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.rc_new_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_rc_new_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.rc_new_top_level,image=self.delete_but_img,
                   command=self.rc_new_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.rc_new_top_level.mainloop()

    def on_close_rc_new_top_level(self):
        self.rc_new_top_level_open = False
        self.rc_new_top_level.destroy()
        self.windows = "closed"

    def rc_new_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def rc_new_status_change(self):
        if self.rc_new_status_var.get() == "0":
            self.rc_new_status_btn.config(image=self.completed_status_img)
            self.rc_new_status_var.set("1")
            print(self.rc_new_status_var.get())
        elif self.rc_new_status_var.get() == "1":
            self.rc_new_status_btn.config(image=self.pending_status_img)
            self.rc_new_status_var.set("0")
            print(self.rc_new_status_var.get())

    def com_rc_new_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.rc_new_priority_var.get()))
        if self.rc_new_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.rc_new_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("rc_new_amount") == None:
                print("1")
                if self.rc_new_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["rc_new_amount"] = self.rc_new_amount_var.get()+","
                    self.data1["rc_new_status"] = self.rc_new_status_var.get()+","
                    self.data1["rc_new_app_no"] = self.rc_new_app_no_var.get()+","
                    self.data1["rc_new_time"] = formatted_time + ","
                    self.data1["rc_new_date"] = formatted_date + ","
                    self.data1["rc_new_priority"] = self.con_value(round(self.rc_new_scale.get()))+","

                    # adding rc_new amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_new_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])


                    res = database.com_rc_new_entry(self.data, self.data1)
                    if res == True:
                        self.rc_new_top_level.destroy()
                        self.on_close_rc_new_top_level()
                        self.update_data(self.all_data,self.data[0])


                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_new_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

            elif self.data1.get("rc_new_amount") != None:
                print("2.0")
                if self.rc_new_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["rc_new_amount"] = self.work_data["rc_new_amount"] +self.rc_new_amount_var.get()+","
                    self.data1["rc_new_status"] = self.work_data["rc_new_status"] +self.rc_new_status_var.get()+","
                    self.data1["rc_new_app_no"] = self.work_data["rc_new_app_no"] +self.rc_new_app_no_var.get()+","

                    self.data1["rc_new_time"] = self.work_data["rc_new_time"] + formatted_time + ","
                    self.data1["rc_new_date"] = self.work_data["rc_new_date"] +formatted_date + ","
                    self.data1["rc_new_priority"] = self.work_data["rc_new_priority"] +self.con_value(round(self.rc_new_scale.get()))+","



                    # adding rc_new amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_new_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_rc_new_entry(self.data, self.data1)
                    if res == True:
                        self.rc_new_top_level.destroy()
                        self.on_close_rc_new_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_new_top_level)
                        print(f"---------=========\n{self.data}")
                        print(f"=========---------\n{self.backup_data}")

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.rc_new_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")
                    data = self.work_data["rc_new_amount"].split(',')
                    # removing old amount of rc_new
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of rc_new
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_new_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])



                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])

                    data = self.work_data["rc_new_amount"].split(',')
                    data[self.index] = self.rc_new_amount_entry.get()
                    data =",".join(data)
                    self.work_data["rc_new_amount"] = data

                    data = self.work_data["rc_new_status"].split(',')
                    data[self.index] = self.rc_new_status_var.get()
                    data =",".join(data)
                    self.work_data["rc_new_status"] = data

                    data = self.work_data["rc_new_app_no"].split(',')
                    data[self.index] = self.rc_new_app_no_var.get()
                    data =",".join(data)
                    self.work_data["rc_new_app_no"] = data


                    data = self.work_data["rc_new_priority"].split(',')
                    data[self.index] = self.con_value(round(self.rc_new_scale.get()))
                    data =",".join(data)
                    self.work_data["rc_new_priority"] = data
                    # messagebox.showinfo(parent=self.rc_new_top_level,title="",message=data)
                    res = database.com_rc_new_entry(self.data, self.work_data)
                    if res == True:
                        self.rc_new_top_level.destroy()
                        self.on_close_rc_new_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_new_top_level)

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_new_combo_fun(self, event):
        if self.rc_new_combo_box.get() == "NEW ENTRY":
            self.rc_new_amount_var.set("")
            self.rc_new_app_no_var.set("")
            self.rc_new_status_var.set("1")
            self.rc_new_status_change()
            self.rc_new_entry_selection_var = "NEW ENTRY"
            self.rc_new_date_lbl.config(text="")
            self.rc_new_time_lbl.config(text="")
            self.rc_new_scale.set(0)


        # self.data[0]["rc_new_amount"]
        else:
            self.rc_new_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.rc_new_combo_box.get())-1
            amount = self.work_data["rc_new_amount"].split(",")
            app_no = self.work_data["rc_new_app_no"].split(",")
            status = self.work_data["rc_new_status"].split(",")
            date = self.work_data["rc_new_date"].split(",")
            time = self.work_data["rc_new_time"].split(",")
            priority = self.work_data["rc_new_priority"].split(",")
            self.rc_new_amount_var.set(amount[int(self.rc_new_combo_box.get())-1])
            self.rc_new_app_no_var.set(app_no[int(self.rc_new_combo_box.get())-1])
            self.rc_new_status_var.set(status[int(self.rc_new_combo_box.get())-1])
            self.rc_new_date_lbl.config(text=date[int(self.rc_new_combo_box.get())-1])
            self.rc_new_time_lbl.config(text=time[int(self.rc_new_combo_box.get())-1])
            self.rc_new_scale.set(self.con_value_rev(priority[int(self.rc_new_combo_box.get())-1]))

            if self.rc_new_status_var.get() == "0":
                self.rc_new_status_btn.config(image=self.pending_status_img)
            elif self.rc_new_status_var.get() == "1":
                self.rc_new_status_btn.config(image=self.completed_status_img)

    def rc_new_entry_delete_fun(self):
        if self.rc_new_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)


            # these three line of code, subtract delete work amount from total
            data = self.work_data["rc_new_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])

            data = self.work_data["rc_new_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_new_amount"] = data

            data = self.work_data["rc_new_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_new_status"] = data

            data = self.work_data["rc_new_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_new_app_no"] = data

            data = self.work_data["rc_new_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_new_date"] = data

            data = self.work_data["rc_new_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_new_time"] = data

            data = self.work_data["rc_new_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_new_priority"] = data

            res = database.com_rc_new_entry(self.data, self.work_data)
            if res == True:
                self.rc_new_top_level.destroy()
                self.on_close_rc_new_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.rc_new_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_new_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.rc_new_update_scale_color(value)  # Update scale color based on value

    def convert_rc_new_app_no_to_uppercase(self):
        current_text = self.rc_new_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.rc_new_app_no_var.set(uppercase_text)

































    def open_rc_renewal_win(self):
        if not self.rc_renewal_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.rc_renewal_top_level_open = True
            self.rc_renewal_top_level = Toplevel()
            self.rc_renewal_top_level.protocol("WM_DELETE_WINDOW", self.on_close_rc_renewal_top_level)
            self.rc_renewal_top_level.configure(bg='#B39CD0')
            screen_width = self.rc_renewal_top_level.winfo_screenwidth()
            screen_height = self.rc_renewal_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.rc_renewal_top_level.title("RC RENEWAL")
            self.rc_renewal_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.rc_renewal_top_level.winfo_screenwidth()
            screen_height = self.rc_renewal_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.rc_renewal_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.rc_renewal_top_level.resizable(False, False)
            self.rc_renewal_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\rc_renewal_bg.png"))
            Label(master=self.rc_renewal_top_level,
                  image=self.rc_renewal_bg_img).pack()

            self.rc_renewal_time_lbl = Label(self.rc_renewal_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.rc_renewal_time_lbl.place(x=75,y=51)

            self.rc_renewal_date_lbl = Label(self.rc_renewal_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.rc_renewal_date_lbl.place(x=195, y=51)

            self.rc_renewal_combo_box = ttk.Combobox(self.rc_renewal_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.rc_renewal_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.rc_renewal_scale = ttk.Scale(self.rc_renewal_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.rc_renewal_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.rc_renewal_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["rc_renewal_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.rc_renewal_combo_box['values'] = self.combo_values

            self.rc_renewal_combo_box.bind('<<ComboboxSelected>>', self.rc_renewal_combo_fun)
            self.rc_renewal_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.rc_renewal_amount_var = StringVar()
            self.rc_renewal_amount_entry = Entry(self.rc_renewal_top_level,
                                                 textvariable=self.rc_renewal_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.rc_renewal_amount_entry.place(x=60, y=125)

            self.rc_renewal_app_no_var = StringVar()
            self.rc_renewal_app_no_entry = Entry(self.rc_renewal_top_level,
                                         textvariable=self.rc_renewal_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.rc_renewal_app_no_entry.place(x=60, y=196)
            self.rc_renewal_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_rc_renewal_app_no_to_uppercase())


            self.rc_renewal_status_var = StringVar()
            self.rc_renewal_status_var.set("0")
            self.rc_renewal_status_btn = Button(master=self.rc_renewal_top_level,
                                                textvariable=self.rc_renewal_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.rc_renewal_status_change,
                                                borderwidth=0
                                                )
            self.rc_renewal_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.rc_renewal_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_rc_renewal_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.rc_renewal_top_level,image=self.delete_but_img,
                   command=self.rc_renewal_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.rc_renewal_top_level.mainloop()

    def on_close_rc_renewal_top_level(self):
        self.rc_renewal_top_level_open = False
        self.rc_renewal_top_level.destroy()
        self.windows = "closed"

    def rc_renewal_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def rc_renewal_status_change(self):
        if self.rc_renewal_status_var.get() == "0":
            self.rc_renewal_status_btn.config(image=self.completed_status_img)
            self.rc_renewal_status_var.set("1")
            print(self.rc_renewal_status_var.get())
        elif self.rc_renewal_status_var.get() == "1":
            self.rc_renewal_status_btn.config(image=self.pending_status_img)
            self.rc_renewal_status_var.set("0")
            print(self.rc_renewal_status_var.get())

    def com_rc_renewal_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.rc_renewal_priority_var.get()))
        if self.rc_renewal_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.rc_renewal_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("rc_renewal_amount") == None:
                print("1")
                if self.rc_renewal_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["rc_renewal_amount"] = self.rc_renewal_amount_var.get()+","
                    self.data1["rc_renewal_status"] = self.rc_renewal_status_var.get()+","
                    self.data1["rc_renewal_app_no"] = self.rc_renewal_app_no_var.get()+","
                    self.data1["rc_renewal_time"] = formatted_time + ","
                    self.data1["rc_renewal_date"] = formatted_date + ","
                    self.data1["rc_renewal_priority"] = self.con_value(round(self.rc_renewal_scale.get()))+","

                    # adding rc_renewal amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_renewal_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])


                    res = database.com_rc_renewal_entry(self.data, self.data1)
                    if res == True:
                        self.rc_renewal_top_level.destroy()
                        self.on_close_rc_renewal_top_level()
                        self.update_data(self.all_data,self.data[0])


                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_renewal_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

            elif self.data1.get("rc_renewal_amount") != None:
                print("2.0")
                if self.rc_renewal_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["rc_renewal_amount"] = self.work_data["rc_renewal_amount"] +self.rc_renewal_amount_var.get()+","
                    self.data1["rc_renewal_status"] = self.work_data["rc_renewal_status"] +self.rc_renewal_status_var.get()+","
                    self.data1["rc_renewal_app_no"] = self.work_data["rc_renewal_app_no"] +self.rc_renewal_app_no_var.get()+","

                    self.data1["rc_renewal_time"] = self.work_data["rc_renewal_time"] + formatted_time + ","
                    self.data1["rc_renewal_date"] = self.work_data["rc_renewal_date"] +formatted_date + ","
                    self.data1["rc_renewal_priority"] = self.work_data["rc_renewal_priority"] +self.con_value(round(self.rc_renewal_scale.get()))+","



                    # adding rc_renewal amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_renewal_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_rc_renewal_entry(self.data, self.data1)
                    if res == True:
                        self.rc_renewal_top_level.destroy()
                        self.on_close_rc_renewal_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_renewal_top_level)
                        print(f"---------=========\n{self.data}")
                        print(f"=========---------\n{self.backup_data}")

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.rc_renewal_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")
                    data = self.work_data["rc_renewal_amount"].split(',')
                    # removing old amount of rc_renewal
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of rc_renewal
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.rc_renewal_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])



                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])

                    data = self.work_data["rc_renewal_amount"].split(',')
                    data[self.index] = self.rc_renewal_amount_entry.get()
                    data =",".join(data)
                    self.work_data["rc_renewal_amount"] = data

                    data = self.work_data["rc_renewal_status"].split(',')
                    data[self.index] = self.rc_renewal_status_var.get()
                    data =",".join(data)
                    self.work_data["rc_renewal_status"] = data

                    data = self.work_data["rc_renewal_app_no"].split(',')
                    data[self.index] = self.rc_renewal_app_no_var.get()
                    data =",".join(data)
                    self.work_data["rc_renewal_app_no"] = data


                    data = self.work_data["rc_renewal_priority"].split(',')
                    data[self.index] = self.con_value(round(self.rc_renewal_scale.get()))
                    data =",".join(data)
                    self.work_data["rc_renewal_priority"] = data
                    # messagebox.showinfo(parent=self.rc_renewal_top_level,title="",message=data)
                    res = database.com_rc_renewal_entry(self.data, self.work_data)
                    if res == True:
                        self.rc_renewal_top_level.destroy()
                        self.on_close_rc_renewal_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.rc_renewal_top_level)

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_renewal_combo_fun(self, event):
        if self.rc_renewal_combo_box.get() == "NEW ENTRY":
            self.rc_renewal_amount_var.set("")
            self.rc_renewal_app_no_var.set("")
            self.rc_renewal_status_var.set("1")
            self.rc_renewal_status_change()
            self.rc_renewal_entry_selection_var = "NEW ENTRY"
            self.rc_renewal_date_lbl.config(text="")
            self.rc_renewal_time_lbl.config(text="")
            self.rc_renewal_scale.set(0)


        # self.data[0]["rc_renewal_amount"]
        else:
            self.rc_renewal_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.rc_renewal_combo_box.get())-1
            amount = self.work_data["rc_renewal_amount"].split(",")
            app_no = self.work_data["rc_renewal_app_no"].split(",")
            status = self.work_data["rc_renewal_status"].split(",")
            date = self.work_data["rc_renewal_date"].split(",")
            time = self.work_data["rc_renewal_time"].split(",")
            priority = self.work_data["rc_renewal_priority"].split(",")
            self.rc_renewal_amount_var.set(amount[int(self.rc_renewal_combo_box.get())-1])
            self.rc_renewal_app_no_var.set(app_no[int(self.rc_renewal_combo_box.get())-1])
            self.rc_renewal_status_var.set(status[int(self.rc_renewal_combo_box.get())-1])
            self.rc_renewal_date_lbl.config(text=date[int(self.rc_renewal_combo_box.get())-1])
            self.rc_renewal_time_lbl.config(text=time[int(self.rc_renewal_combo_box.get())-1])
            self.rc_renewal_scale.set(self.con_value_rev(priority[int(self.rc_renewal_combo_box.get())-1]))

            if self.rc_renewal_status_var.get() == "0":
                self.rc_renewal_status_btn.config(image=self.pending_status_img)
            elif self.rc_renewal_status_var.get() == "1":
                self.rc_renewal_status_btn.config(image=self.completed_status_img)

    def rc_renewal_entry_delete_fun(self):
        if self.rc_renewal_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)


            # these three line of code, subtract delete work amount from total
            data = self.work_data["rc_renewal_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])

            data = self.work_data["rc_renewal_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_renewal_amount"] = data

            data = self.work_data["rc_renewal_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_renewal_status"] = data

            data = self.work_data["rc_renewal_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_renewal_app_no"] = data

            data = self.work_data["rc_renewal_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_renewal_date"] = data

            data = self.work_data["rc_renewal_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_renewal_time"] = data

            data = self.work_data["rc_renewal_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["rc_renewal_priority"] = data

            res = database.com_rc_renewal_entry(self.data, self.work_data)
            if res == True:
                self.rc_renewal_top_level.destroy()
                self.on_close_rc_renewal_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.rc_renewal_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def rc_renewal_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.rc_renewal_update_scale_color(value)  # Update scale color based on value

    def convert_rc_renewal_app_no_to_uppercase(self):
        current_text = self.rc_renewal_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.rc_renewal_app_no_var.set(uppercase_text)



























    def open_new_registration_win(self):
        if not self.new_registration_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.new_registration_top_level_open = True
            self.new_registration_top_level = Toplevel()
            self.new_registration_top_level.protocol("WM_DELETE_WINDOW", self.on_close_new_registration_top_level)
            self.new_registration_top_level.configure(bg='#B39CD0')
            screen_width = self.new_registration_top_level.winfo_screenwidth()
            screen_height = self.new_registration_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.new_registration_top_level.title("NEW REGISTRATION")
            self.new_registration_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.new_registration_top_level.winfo_screenwidth()
            screen_height = self.new_registration_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.new_registration_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.new_registration_top_level.resizable(False, False)
            self.new_registration_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\new_registration_bg.png"))
            Label(master=self.new_registration_top_level,
                  image=self.new_registration_bg_img).pack()

            self.new_registration_time_lbl = Label(self.new_registration_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.new_registration_time_lbl.place(x=75,y=51)

            self.new_registration_date_lbl = Label(self.new_registration_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.new_registration_date_lbl.place(x=195, y=51)

            self.new_registration_combo_box = ttk.Combobox(self.new_registration_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.new_registration_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.new_registration_scale = ttk.Scale(self.new_registration_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.new_registration_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.new_registration_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["new_registration_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.new_registration_combo_box['values'] = self.combo_values

            self.new_registration_combo_box.bind('<<ComboboxSelected>>', self.new_registration_combo_fun)
            self.new_registration_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.new_registration_amount_var = StringVar()
            self.new_registration_amount_entry = Entry(self.new_registration_top_level,
                                                 textvariable=self.new_registration_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.new_registration_amount_entry.place(x=60, y=125)

            self.new_registration_app_no_var = StringVar()
            self.new_registration_app_no_entry = Entry(self.new_registration_top_level,
                                         textvariable=self.new_registration_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.new_registration_app_no_entry.place(x=60, y=196)
            self.new_registration_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_new_registration_app_no_to_uppercase())


            self.new_registration_status_var = StringVar()
            self.new_registration_status_var.set("0")
            self.new_registration_status_btn = Button(master=self.new_registration_top_level,
                                                textvariable=self.new_registration_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.new_registration_status_change,
                                                borderwidth=0
                                                )
            self.new_registration_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.new_registration_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_new_registration_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.new_registration_top_level,image=self.delete_but_img,
                   command=self.new_registration_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.new_registration_top_level.mainloop()

    def on_close_new_registration_top_level(self):
        self.new_registration_top_level_open = False
        self.new_registration_top_level.destroy()
        self.windows = "closed"

    def new_registration_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def new_registration_status_change(self):
        if self.new_registration_status_var.get() == "0":
            self.new_registration_status_btn.config(image=self.completed_status_img)
            self.new_registration_status_var.set("1")
            print(self.new_registration_status_var.get())
        elif self.new_registration_status_var.get() == "1":
            self.new_registration_status_btn.config(image=self.pending_status_img)
            self.new_registration_status_var.set("0")
            print(self.new_registration_status_var.get())

    def com_new_registration_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.new_registration_priority_var.get()))
        if self.new_registration_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.new_registration_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("new_registration_amount") == None:
                print("1")
                if self.new_registration_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["new_registration_amount"] = self.new_registration_amount_var.get()+","
                    self.data1["new_registration_status"] = self.new_registration_status_var.get()+","
                    self.data1["new_registration_app_no"] = self.new_registration_app_no_var.get()+","
                    self.data1["new_registration_time"] = formatted_time + ","
                    self.data1["new_registration_date"] = formatted_date + ","
                    self.data1["new_registration_priority"] = self.con_value(round(self.new_registration_scale.get()))+","

                    # adding new_registration amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.new_registration_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])


                    res = database.com_new_registration_entry(self.data, self.data1)
                    if res == True:
                        self.new_registration_top_level.destroy()
                        self.on_close_new_registration_top_level()
                        self.update_data(self.all_data,self.data[0])


                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.new_registration_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

            elif self.data1.get("new_registration_amount") != None:
                print("2.0")
                if self.new_registration_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["new_registration_amount"] = self.work_data["new_registration_amount"] +self.new_registration_amount_var.get()+","
                    self.data1["new_registration_status"] = self.work_data["new_registration_status"] +self.new_registration_status_var.get()+","
                    self.data1["new_registration_app_no"] = self.work_data["new_registration_app_no"] +self.new_registration_app_no_var.get()+","

                    self.data1["new_registration_time"] = self.work_data["new_registration_time"] + formatted_time + ","
                    self.data1["new_registration_date"] = self.work_data["new_registration_date"] +formatted_date + ","
                    self.data1["new_registration_priority"] = self.work_data["new_registration_priority"] +self.con_value(round(self.new_registration_scale.get()))+","



                    # adding new_registration amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.new_registration_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_new_registration_entry(self.data, self.data1)
                    if res == True:
                        self.new_registration_top_level.destroy()
                        self.on_close_new_registration_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.new_registration_top_level)
                        print(f"---------=========\n{self.data}")
                        print(f"=========---------\n{self.backup_data}")

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.new_registration_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")
                    data = self.work_data["new_registration_amount"].split(',')
                    # removing old amount of new_registration
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of new_registration
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.new_registration_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])



                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])

                    data = self.work_data["new_registration_amount"].split(',')
                    data[self.index] = self.new_registration_amount_entry.get()
                    data =",".join(data)
                    self.work_data["new_registration_amount"] = data

                    data = self.work_data["new_registration_status"].split(',')
                    data[self.index] = self.new_registration_status_var.get()
                    data =",".join(data)
                    self.work_data["new_registration_status"] = data

                    data = self.work_data["new_registration_app_no"].split(',')
                    data[self.index] = self.new_registration_app_no_var.get()
                    data =",".join(data)
                    self.work_data["new_registration_app_no"] = data


                    data = self.work_data["new_registration_priority"].split(',')
                    data[self.index] = self.con_value(round(self.new_registration_scale.get()))
                    data =",".join(data)
                    self.work_data["new_registration_priority"] = data
                    # messagebox.showinfo(parent=self.new_registration_top_level,title="",message=data)
                    res = database.com_new_registration_entry(self.data, self.work_data)
                    if res == True:
                        self.new_registration_top_level.destroy()
                        self.on_close_new_registration_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.new_registration_top_level)

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def new_registration_combo_fun(self, event):
        if self.new_registration_combo_box.get() == "NEW ENTRY":
            self.new_registration_amount_var.set("")
            self.new_registration_app_no_var.set("")
            self.new_registration_status_var.set("1")
            self.new_registration_status_change()
            self.new_registration_entry_selection_var = "NEW ENTRY"
            self.new_registration_date_lbl.config(text="")
            self.new_registration_time_lbl.config(text="")
            self.new_registration_scale.set(0)


        # self.data[0]["new_registration_amount"]
        else:
            self.new_registration_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.new_registration_combo_box.get())-1
            amount = self.work_data["new_registration_amount"].split(",")
            app_no = self.work_data["new_registration_app_no"].split(",")
            status = self.work_data["new_registration_status"].split(",")
            date = self.work_data["new_registration_date"].split(",")
            time = self.work_data["new_registration_time"].split(",")
            priority = self.work_data["new_registration_priority"].split(",")
            self.new_registration_amount_var.set(amount[int(self.new_registration_combo_box.get())-1])
            self.new_registration_app_no_var.set(app_no[int(self.new_registration_combo_box.get())-1])
            self.new_registration_status_var.set(status[int(self.new_registration_combo_box.get())-1])
            self.new_registration_date_lbl.config(text=date[int(self.new_registration_combo_box.get())-1])
            self.new_registration_time_lbl.config(text=time[int(self.new_registration_combo_box.get())-1])
            self.new_registration_scale.set(self.con_value_rev(priority[int(self.new_registration_combo_box.get())-1]))

            if self.new_registration_status_var.get() == "0":
                self.new_registration_status_btn.config(image=self.pending_status_img)
            elif self.new_registration_status_var.get() == "1":
                self.new_registration_status_btn.config(image=self.completed_status_img)

    def new_registration_entry_delete_fun(self):
        if self.new_registration_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)


            # these three line of code, subtract delete work amount from total
            data = self.work_data["new_registration_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])

            data = self.work_data["new_registration_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["new_registration_amount"] = data

            data = self.work_data["new_registration_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["new_registration_status"] = data

            data = self.work_data["new_registration_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["new_registration_app_no"] = data

            data = self.work_data["new_registration_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["new_registration_date"] = data

            data = self.work_data["new_registration_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["new_registration_time"] = data

            data = self.work_data["new_registration_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["new_registration_priority"] = data

            res = database.com_new_registration_entry(self.data, self.work_data)
            if res == True:
                self.new_registration_top_level.destroy()
                self.on_close_new_registration_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.new_registration_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def new_registration_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.new_registration_update_scale_color(value)  # Update scale color based on value

    def convert_new_registration_app_no_to_uppercase(self):
        current_text = self.new_registration_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.new_registration_app_no_var.set(uppercase_text)

































    def open_others_work_win(self):
        if not self.others_work_top_level_open and self.windows == "closed":
            self.windows = "open"
            self.others_work_top_level_open = True
            self.others_work_top_level = Toplevel()
            self.others_work_top_level.protocol("WM_DELETE_WINDOW", self.on_close_others_work_top_level)
            self.others_work_top_level.configure(bg='#B39CD0')
            screen_width = self.others_work_top_level.winfo_screenwidth()
            screen_height = self.others_work_top_level.winfo_screenheight()
            print(f"{screen_height}x{screen_width}")
            self.others_work_top_level.title("OTHERS WORK")
            self.others_work_top_level.attributes('-topmost', True)
            app_width = 500
            app_height = 500
            screen_width = self.others_work_top_level.winfo_screenwidth()
            screen_height = self.others_work_top_level.winfo_screenheight()
            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height / 2 + 28)

            self.others_work_top_level.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
            self.others_work_top_level.resizable(False, False)
            self.others_work_bg_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\others_work_bg.png"))
            Label(master=self.others_work_top_level,
                  image=self.others_work_bg_img).pack()

            self.others_work_time_lbl = Label(self.others_work_top_level, bg="#3b0085",
                                             foreground="white", text="", font=("helvatica", self.label_size, "bold"))
            self.others_work_time_lbl.place(x=75,y=51)

            self.others_work_date_lbl = Label(self.others_work_top_level, bg="#3b0085",
                                             foreground="white",text="", font=("helvatica", self.label_size, "bold"))
            self.others_work_date_lbl.place(x=195, y=51)

            self.others_work_combo_box = ttk.Combobox(self.others_work_top_level,font=("helvatica", self.combobox_size, "bold"),
                                                     width=self.combobox_width,
                                                     state="readonly")
            self.others_work_combo_box.place(x=307, y=53)

            self.style = ttk.Style()
            self.style.theme_use('default')
            self.style.configure("Custom.Horizontal.TScale", background="#f0f0f0", troughcolor="#dcdcdc", sliderthickness=10,
                            sliderlength=50)
            # Create a Scale widget using ttk
            self.others_work_scale = ttk.Scale(self.others_work_top_level, from_=0, to=2, orient=HORIZONTAL,
                              command=self.others_work_on_scale_change,
                              style="Custom.Horizontal.TScale")
            self.others_work_scale.place(x=335, y=135)
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])


            self.combo_values = ["NEW ENTRY",]
            try:
                data = self.work_data["others_work_amount"]
                split_data = data.split(',')
                self.combo_values += [i+1 for i in range(len(split_data)-1)]
            except:
                pass
            self.others_work_combo_box['values'] = self.combo_values

            self.others_work_combo_box.bind('<<ComboboxSelected>>', self.others_work_combo_fun)
            self.others_work_entry_selection_var = "NEW ENTRY"
            print(f"values {self.combo_values}")
            self.others_work_amount_var = StringVar()
            self.others_work_amount_entry = Entry(self.others_work_top_level,
                                                 textvariable=self.others_work_amount_var,
                                                 bg=self.color_1,
                                                 # disabledbackground=self.color_1,
                                                 validate="key",
                                                 validatecommand=(self.main_root.register(self.validate_amount),
                                                                  "%S"),
                                                 border=0,
                                                 width=self.field_width_2,
                                                 font=("Helvetica", self.font_size))
            self.others_work_amount_entry.place(x=60, y=125)

            self.others_work_app_no_var = StringVar()
            self.others_work_app_no_entry = Entry(self.others_work_top_level,
                                         textvariable=self.others_work_app_no_var,
                                         validate="key",
                                         validatecommand=(self.main_root.register(self.validate_data), "%P"),
                                         width=self.field_width_2,
                                         bg=self.color_1,
                                         border=0,
                                         font=("Helvetica", self.font_size))
            self.others_work_app_no_entry.place(x=60, y=196)
            self.others_work_app_no_entry.bind('<KeyRelease>', lambda event: self.convert_others_work_app_no_to_uppercase())


            self.others_work_status_var = StringVar()
            self.others_work_status_var.set("0")
            self.others_work_status_btn = Button(master=self.others_work_top_level,
                                                textvariable=self.others_work_status_var,
                                                image=self.pending_status_img,
                                                bg=self.bg_color,
                                                activebackground=self.bg_color,
                                                command=self.others_work_status_change,
                                                borderwidth=0
                                                )
            self.others_work_status_btn.place(x=250, y=125)

            self.submit_but_img = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))
            Button(master=self.others_work_top_level,text="submit",
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0,
                   image=self.submit_but_img,
                   command=self.com_others_work_entry_fun).place(x=150, y=420)


            self.delete_but_img = ImageTk.PhotoImage(Image.open(r"images\all_work_img\delete_but.png"))
            Button(master=self.others_work_top_level,image=self.delete_but_img,
                   command=self.others_work_entry_delete_fun,
                   bg=self.bg_color,
                   activebackground=self.bg_color,
                   borderwidth=0

                   ).place(x=290, y=125)


            self.others_work_top_level.mainloop()

    def on_close_others_work_top_level(self):
        self.others_work_top_level_open = False
        self.others_work_top_level.destroy()
        self.windows = "closed"

    def others_work_update_scale_color(self,value):
        # Update the color of the scale based on its value
        if value == 0:  # Low
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#00ff00'), ('pressed', '#00ff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 1:  # Medium
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ffff00'), ('pressed', '#ffff00')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])
        elif value == 2:  # High
            self.style.map("Custom.Horizontal.TScale",
                      background=[(f'!active', '#ff0000'), ('pressed', '#ff0000')],
                      troughcolor=[('!active', '#dcdcdc'), ('pressed', '#dcdcdc')])

    def others_work_status_change(self):
        if self.others_work_status_var.get() == "0":
            self.others_work_status_btn.config(image=self.completed_status_img)
            self.others_work_status_var.set("1")
            print(self.others_work_status_var.get())
        elif self.others_work_status_var.get() == "1":
            self.others_work_status_btn.config(image=self.pending_status_img)
            self.others_work_status_var.set("0")
            print(self.others_work_status_var.get())

    def com_others_work_entry_fun(self):
        self.backup_data = copy.deepcopy(self.data)
        # print(type(self.others_work_priority_var.get()))
        if self.others_work_amount_var.get() == "":
            messagebox.showwarning(title="Empty Field",message="Please Enter Amount",parent=self.others_work_top_level)
        else:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")
            # Set the locale to English (United States)
            current_time = datetime.now().time()
            formatted_time = current_time.strftime("%I:%M:%S %p")
            print(type(self.data))
            self.data1 = self.work_data

            # result_data[0]["name"]
            if self.data1.get("others_work_amount") == None:
                print("1")
                if self.others_work_entry_selection_var == "NEW ENTRY":
                    print("1.1")
                    self.data1["others_work_amount"] = self.others_work_amount_var.get()+","
                    self.data1["others_work_status"] = self.others_work_status_var.get()+","
                    self.data1["others_work_app_no"] = self.others_work_app_no_var.get()+","
                    self.data1["others_work_time"] = formatted_time + ","
                    self.data1["others_work_date"] = formatted_date + ","
                    self.data1["others_work_priority"] = self.con_value(round(self.others_work_scale.get()))+","

                    # adding others_work amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.others_work_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])


                    res = database.com_others_work_entry(self.data, self.data1)
                    if res == True:
                        self.others_work_top_level.destroy()
                        self.on_close_others_work_top_level()
                        self.update_data(self.all_data,self.data[0])


                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.others_work_top_level)
                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

            elif self.data1.get("others_work_amount") != None:
                print("2.0")
                if self.others_work_entry_selection_var == "NEW ENTRY":
                    print("2.1")
                    self.data1["others_work_amount"] = self.work_data["others_work_amount"] +self.others_work_amount_var.get()+","
                    self.data1["others_work_status"] = self.work_data["others_work_status"] +self.others_work_status_var.get()+","
                    self.data1["others_work_app_no"] = self.work_data["others_work_app_no"] +self.others_work_app_no_var.get()+","

                    self.data1["others_work_time"] = self.work_data["others_work_time"] + formatted_time + ","
                    self.data1["others_work_date"] = self.work_data["others_work_date"] +formatted_date + ","
                    self.data1["others_work_priority"] = self.work_data["others_work_priority"] +self.con_value(round(self.others_work_scale.get()))+","



                    # adding others_work amount + total amount in local data
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.others_work_amount_var.get())

                    # updating total amount in gui
                    self.total_amount_var.set(self.data[0]["total_amount"])

                    # calculating due amount = total_amount - recieved_amount
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]

                    # updating due amount in gui
                    self.due_amount_var.set(self.data[0]["due_amount"])



                    res = database.com_others_work_entry(self.data, self.data1)
                    if res == True:
                        self.others_work_top_level.destroy()
                        self.on_close_others_work_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.others_work_top_level)
                        print(f"---------=========\n{self.data}")
                        print(f"=========---------\n{self.backup_data}")

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])

                elif self.others_work_entry_selection_var == "MODIFY ENTRY":
                    print("2.2")
                    data = self.work_data["others_work_amount"].split(',')
                    # removing old amount of others_work
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
                    # adding new amount of others_work
                    self.data[0]["total_amount"] = self.data[0]["total_amount"] + int(self.others_work_amount_var.get())
                    # setting up in total amount
                    self.total_amount_var.set(self.data[0]["total_amount"])



                    # setup total due amount in offline data and also updating it in gui
                    self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
                    self.due_amount_var.set(self.data[0]["due_amount"])

                    data = self.work_data["others_work_amount"].split(',')
                    data[self.index] = self.others_work_amount_entry.get()
                    data =",".join(data)
                    self.work_data["others_work_amount"] = data

                    data = self.work_data["others_work_status"].split(',')
                    data[self.index] = self.others_work_status_var.get()
                    data =",".join(data)
                    self.work_data["others_work_status"] = data

                    data = self.work_data["others_work_app_no"].split(',')
                    data[self.index] = self.others_work_app_no_var.get()
                    data =",".join(data)
                    self.work_data["others_work_app_no"] = data


                    data = self.work_data["others_work_priority"].split(',')
                    data[self.index] = self.con_value(round(self.others_work_scale.get()))
                    data =",".join(data)
                    self.work_data["others_work_priority"] = data
                    # messagebox.showinfo(parent=self.others_work_top_level,title="",message=data)
                    res = database.com_others_work_entry(self.data, self.work_data)
                    if res == True:
                        self.others_work_top_level.destroy()
                        self.on_close_others_work_top_level()
                        self.update_data(self.all_data,self.data[0])

                    elif res == False:
                        messagebox.showerror(title="Error", message="Please Check Your internet",
                                               parent=self.others_work_top_level)

                        self.data[0].update(self.backup_data[0])
                        self.total_amount_var.set(self.data[0]["total_amount"])
                        self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                        self.due_amount_var.set(self.data[0]["due_amount"])
    def others_work_combo_fun(self, event):
        if self.others_work_combo_box.get() == "NEW ENTRY":
            self.others_work_amount_var.set("")
            self.others_work_app_no_var.set("")
            self.others_work_status_var.set("1")
            self.others_work_status_change()
            self.others_work_entry_selection_var = "NEW ENTRY"
            self.others_work_date_lbl.config(text="")
            self.others_work_time_lbl.config(text="")
            self.others_work_scale.set(0)


        # self.data[0]["others_work_amount"]
        else:
            self.others_work_entry_selection_var = "MODIFY ENTRY"
            self.index = int(self.others_work_combo_box.get())-1
            amount = self.work_data["others_work_amount"].split(",")
            app_no = self.work_data["others_work_app_no"].split(",")
            status = self.work_data["others_work_status"].split(",")
            date = self.work_data["others_work_date"].split(",")
            time = self.work_data["others_work_time"].split(",")
            priority = self.work_data["others_work_priority"].split(",")
            self.others_work_amount_var.set(amount[int(self.others_work_combo_box.get())-1])
            self.others_work_app_no_var.set(app_no[int(self.others_work_combo_box.get())-1])
            self.others_work_status_var.set(status[int(self.others_work_combo_box.get())-1])
            self.others_work_date_lbl.config(text=date[int(self.others_work_combo_box.get())-1])
            self.others_work_time_lbl.config(text=time[int(self.others_work_combo_box.get())-1])
            self.others_work_scale.set(self.con_value_rev(priority[int(self.others_work_combo_box.get())-1]))

            if self.others_work_status_var.get() == "0":
                self.others_work_status_btn.config(image=self.pending_status_img)
            elif self.others_work_status_var.get() == "1":
                self.others_work_status_btn.config(image=self.completed_status_img)

    def others_work_entry_delete_fun(self):
        if self.others_work_combo_box.get().isdigit(): #condition checks that if entry available then only deletion works
            self.backup_data = copy.deepcopy(self.data)


            # these three line of code, subtract delete work amount from total
            data = self.work_data["others_work_amount"].split(',')
            self.data[0]["total_amount"] = self.data[0]["total_amount"] - int(data[self.index])
            self.total_amount_var.set(self.data[0]["total_amount"])

            # setup total due amount in offline data and also updating it in gui
            self.data[0]["due_amount"] = self.data[0]["total_amount"] - self.data[0]["recieved_amount"]
            self.due_amount_var.set(self.data[0]["due_amount"])

            data = self.work_data["others_work_amount"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["others_work_amount"] = data

            data = self.work_data["others_work_status"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["others_work_status"] = data

            data = self.work_data["others_work_app_no"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["others_work_app_no"] = data

            data = self.work_data["others_work_date"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["others_work_date"] = data

            data = self.work_data["others_work_time"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["others_work_time"] = data

            data = self.work_data["others_work_priority"].split(',')
            data.pop(self.index)
            data = ",".join(data)
            self.work_data["others_work_priority"] = data

            res = database.com_others_work_entry(self.data, self.work_data)
            if res == True:
                self.others_work_top_level.destroy()
                self.on_close_others_work_top_level()
                self.update_data(self.all_data, self.data[0])

            elif res == False:
                messagebox.showerror(title="Error", message="Please Check Your internet",
                                     parent=self.others_work_top_level)
                self.data[0].update(self.backup_data[0])
                self.total_amount_var.set(self.data[0]["total_amount"])
                self.recieved_amount_var.set(self.data[0]["recieved_amount"])
                self.due_amount_var.set(self.data[0]["due_amount"])
    def others_work_on_scale_change(self,value):
        # This function will be called whenever the slider's value changes
        # Convert the value to an integer rounded to the nearest whole number
        value = round(float(value))
        self.others_work_update_scale_color(value)  # Update scale color based on value

    def convert_others_work_app_no_to_uppercase(self):
        current_text = self.others_work_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.others_work_app_no_var.set(uppercase_text)






















    def validate_amount(self, char):
        # Check if the input is a digit
        return char.isdigit() or char == ""

    def validate_name(self, string):
        """for validate user can enter name or spaces in between name and sir name  """

        pattern = "^[a-zA-Z][a-zA-Z\s]*$"
        if re.match(pattern, string) or string == "":
            print(f'Accepted: {string}')
            return True
        else:
            print(f'Rejected: {string}')
            return False
    def rc_transfer_to_uppercase(self):
        current_text = self.rc_transfer_name_var.get()
        uppercase_text = current_text.upper()
        self.rc_transfer_name_var.set(uppercase_text)

    def validate_data(self, data):
        pattern = r'^[a-zA-Z0-9\s]*$'
        if re.match(pattern, data) or data == "":
            print(f'Accepted: {data}')
            return True
        else:
            print(f'Rejected: {data}')
            return False

    def convert_reassign_app_no_to_uppercase(self):
        current_text = self.re_assign_app_no_var.get()
        uppercase_text = current_text.upper()
        self.re_assign_app_no_var.set(uppercase_text)

    def convert_re_assign_new_no_to_uppercase(self):
        current_text = self.re_assign_new_no_var.get()
        uppercase_text = current_text.upper()
        self.re_assign_new_no_var.set(uppercase_text)


    def convert_noc_sent_state_to_uppercase(self):
        current_text = self.noc_sent_state_entry.get()
        uppercase_text = current_text.upper()
        self.noc_sent_state_var.set(uppercase_text)

    def convert_noc_sent_district_to_uppercase(self):
        current_text = self.noc_sent_district_entry.get()
        uppercase_text = current_text.upper()
        self.noc_sent_district_var.set(uppercase_text)


    def convert_noc_sent_app_no_to_uppercase(self):
        current_text = self.noc_sent_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.noc_sent_app_no_var.set(uppercase_text)

    def convert_noc_accept_state_to_uppercase(self):
        current_text = self.noc_accept_state_entry.get()
        uppercase_text = current_text.upper()
        self.noc_accept_state_var.set(uppercase_text)

    def convert_noc_accept_district_to_uppercase(self):
        current_text = self.noc_accept_district_entry.get()
        uppercase_text = current_text.upper()
        self.noc_accept_district_var.set(uppercase_text)
    def convert_noc_accept_app_no_to_uppercase(self):
        current_text = self.noc_accept_app_no_entry.get()
        uppercase_text = current_text.upper()
        self.noc_accept_app_no_var.set(uppercase_text)


    def back_but_fun(self):
        import home
        for widget in self.main_root.winfo_children():
            print(widget)
            widget.destroy()
        del self.icon
        del self.image
        del self.back_btn_img
        del self.pending_btn_img
        del self.payment_btn_img

        del self.pending_status_img
        del self.completed_status_img
        del self.new1
        del self.new2
        del self.new1_1
        del self.new2_2
        del self.edit_btn_img
        del self.editing_done_btn_img
        # # del self.rc_redispatch_img
        # del self.rc_duplicate_img
        # del self.rc_modify_img
        # del self.rc_transfer_img
        # del self.rc_conversion_img
        # del self.hp_cancel_img
        # del self.hp_made_img
        # del self.hsrp_img
        # del self.fitness_img
        # del self.insurance_img
        # del self.pb_late_fine_img
        # del self.np_late_fine_img
        # del self.pb_permit_new_img
        # del self.np_permit_img
        # del self.alteration_img
        # del self.tax_img
        # del self.tax_no_due_img
        # del self.reassignment_img
        # del self.noc_sent_img
        # del self.noc_accept_img
        # del self.pb_surrender_img
        # del self.np_surrender_img
        # del self.pollution_img
        # del self.address_change_img
        # del self.fancy_number_img
        # del self.phone_change_img
        # del self.np_authorization_img
        # del self.rc_new_img
        # del self.rc_renewal_img
        # del self.new_registration_img
        # del self.others_work_img



        self.main_root.destroy()
        obj = home.Main()
        obj.Home(self.all_data)

    def a(self):
        self.vehicle_type.set("commercial")
        self.b1.config(image=self.new1_1)
        self.b2.config(image=self.new2)

    def b(self):
        self.vehicle_type.set("private")
        self.b2.config(image=self.new2_2)
        self.b1.config(image=self.new1)



        # self.two_wheeler_radio_btn.place(x=550, y=0)
        # self.four_wheeler_radio_btn.place(x=670, y=0)

    def convert_name_to_uppercase(self):
        current_text = self.name_var.get()
        uppercase_text = current_text.upper()
        self.name_var.set(uppercase_text)

    def convert_numberplate_to_uppercase(self):

        current_text = self.numberplate_no_var.get()
        uppercase_text = current_text.upper()
        self.numberplate_no_var.set(uppercase_text)

    def convert_car_model_to_uppercase(self):
        current_text = self.car_model_var.get()
        uppercase_text = current_text.upper()
        self.car_model_var.set(uppercase_text)

    def convert_engine_no_to_uppercase(self):
        current_text = self.engine_var.get()
        uppercase_text = current_text.upper()
        self.engine_var.set(uppercase_text)

    def convert_chassis_no_to_uppercase(self):
        current_text = self.chassis_no_var.get()
        uppercase_text = current_text.upper()
        self.chassis_no_var.set(uppercase_text)

    def validate_phone(self, phone_number):
        # Define the regular expression pattern for a 10-digit phone number

        return re.match(r'^\d{0,10}$', phone_number) is not None

    # --------------------------------------PENDING DOCS---------------------------------

    def pending_doc_win(self):
        if not self.pending_window:
            self.pending_window = True
            self.pending_root = Toplevel()
            self.pending_root.protocol("WM_DELETE_WINDOW", self.on_close_pending_window)
            self.pending_root.title("Pending Docs")
            self.app_width = 700
            self.app_height = 500
            self.screen_width = self.pending_root.winfo_screenwidth()
            self.screen_height = self.pending_root.winfo_screenheight()
            self.x = (self.screen_width / 2) - (self.app_width / 2)
            self.y = (self.screen_height / 2) - (self.app_height / 2 + 35)
            self.pending_root.geometry(f"{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}")
            self.pending_root.resizable(False, False)
            self.image1 = Image.open("images\pending_doc\pending_doc_bg.png")
            self.photo1 = ImageTk.PhotoImage(image=self.image1)
            self.img_lbl1 = Label(self.pending_root, image=self.photo1)
            self.img_lbl1.place(x=-2, y=0)

            self.pb_new_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\pb_new_gray.png"))
            self.pb_new_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\pb_new_green.png"))
            self.pb_new_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\pb_new_red.png"))
            self.pb_permit_new_Var1 = IntVar()
            self.pb_permit_new_chk_box1 = Button(self.pending_root, textvariable=self.pb_permit_new_Var1,
                                                bg="#B39CD0",
                                                activebackground="#B39CD0",
                                                borderwidth=0,
                                                command=self.pb_permit_change,
                                                )
            self.pb_permit_new_chk_box1.place(x=16, y=72)
            if self.pending_data == []:
                self.pb_permit_new_chk_box1.config(image=self.pb_new_gray)
            elif len(self.pending_data) == 12 and self.pending_data[0] !=0:
                if self.pending_data[0] == 0:
                    self.pb_permit_new_Var1.set(0)
                    self.pb_permit_new_chk_box1.config(image=self.pb_new_gray)
                elif self.pending_data[0] == 1:
                    self.pb_permit_new_Var1.set(1)
                    self.pb_permit_new_chk_box1.config(image=self.pb_new_green)
                elif self.pending_data[0] == 2:
                    self.pb_permit_new_Var1.set(2)
                    self.pb_permit_new_chk_box1.config(image=self.pb_new_red)
            elif self.pending_data[0] == 0:
                self.pb_permit_new_Var1.set(0)
                self.pb_permit_new_chk_box1.config(image=self.pb_new_gray)




            self.np_permit_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\np_permit_gray.png"))
            self.np_permit_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\np_permit_green.png"))
            self.np_permit_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\np_permit_red.png"))

            self.np_permit_Var1 = IntVar()
            self.np_permit_chk_box1 = Button(self.pending_root, textvariable=self.np_permit_Var1,
                                            image=self.np_permit_gray,
                                            bg="#B39CD0",
                                            activebackground="#B39CD0",
                                            borderwidth=0,
                                            command=self.np_permit_change,
                                            )
            self.np_permit_chk_box1.place(x=259, y=72)
            if self.pending_data == []:
                self.np_permit_chk_box1.config(image=self.np_permit_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[1] == 0:
                    self.np_permit_Var1.set(0)
                    self.np_permit_chk_box1.config(image=self.np_permit_gray)
                elif self.pending_data[1] == 1:
                    self.np_permit_Var1.set(1)
                    self.np_permit_chk_box1.config(image=self.np_permit_green)
                elif self.pending_data[1] == 2:
                    self.np_permit_Var1.set(2)
                    self.np_permit_chk_box1.config(image=self.np_permit_red)
            elif self.pending_data[1] == 0:
                self.np_permit_Var1.set(0)
                self.np_permit_chk_box1.config(image=self.np_permit_gray)




            self.bank_noc_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\bank_noc_gray.png"))
            self.bank_noc_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\bank_noc_green.png"))
            self.bank_noc_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\bank_noc_red.png"))
            self.bank_noc_Var1 = IntVar()
            self.bank_noc_chk_box1 = Button(self.pending_root, textvariable=self.bank_noc_Var1,
                                           image=self.bank_noc_gray,
                                           bg="#B39CD0",
                                           activebackground="#B39CD0",
                                           borderwidth=0,
                                           command=self.bank_noc_change,
                                           )
            self.bank_noc_chk_box1.place(x=502, y=72)
            if self.pending_data == []:
                self.bank_noc_chk_box1.config(image=self.bank_noc_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[2] == 0:
                    self.bank_noc_Var1.set(0)
                    self.bank_noc_chk_box1.config(image=self.bank_noc_gray)
                elif self.pending_data[2] == 1:
                    self.bank_noc_Var1.set(1)
                    self.bank_noc_chk_box1.config(image=self.bank_noc_green)
                elif self.pending_data[2] == 2:
                    self.bank_noc_Var1.set(2)
                    self.bank_noc_chk_box1.config(image=self.bank_noc_red)
            elif self.pending_data[2] == 0:
                self.bank_noc_Var1.set(0)
                self.bank_noc_chk_box1.config(image=self.bank_noc_gray)
            self.seller_aff_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\seller_aff_gray.png"))
            self.seller_aff_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\seller_aff_green.png"))
            self.seller_aff_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\seller_aff_red.png"))
            self.seller_affidavit_Var = IntVar()
            self.seller_affidavit_chk_box = Button(self.pending_root, textvariable=self.seller_affidavit_Var,
                                                   image=self.seller_aff_gray,
                                                   bg="#B39CD0",
                                                   activebackground="#B39CD0",
                                                   borderwidth=0,
                                                   command=self.seller_aff_change,
                                                   )
            self.seller_affidavit_chk_box.place(x=16, y=110)
            if self.pending_data == []:
                self.seller_affidavit_chk_box.config(image=self.seller_aff_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[3] == 0:
                    self.seller_affidavit_Var.set(0)
                    self.seller_affidavit_chk_box.config(image=self.seller_aff_gray)
                elif self.pending_data[3] == 1:
                    self.seller_affidavit_Var.set(1)
                    self.seller_affidavit_chk_box.config(image=self.seller_aff_green)
                elif self.pending_data[3] == 2:
                    self.seller_affidavit_Var.set(2)
                    self.seller_affidavit_chk_box.config(image=self.seller_aff_red)
            elif self.pending_data[3] == 0:
                self.seller_affidavit_Var.set(0)
                self.seller_affidavit_chk_box.config(image=self.seller_aff_gray)

            self.purchaser_aff_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\purchaser_aff_gray.png"))
            self.purchaser_aff_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\purchaser_aff_green.png"))
            self.purchaser_aff_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\purchaser_aff_red.png"))
            self.purchaser_affidavit_Var = IntVar()
            self.purchaser_affidavit_chk_box = Button(self.pending_root, textvariable=self.purchaser_affidavit_Var,
                                                      image=self.purchaser_aff_gray,
                                                      bg="#B39CD0",
                                                      activebackground="#B39CD0",
                                                      borderwidth=0,
                                                      command=self.purchaser_aff_change,
                                                      )
            self.purchaser_affidavit_chk_box.place(x=259, y=110)
            if self.pending_data == []:
                self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[4] == 0:
                    self.purchaser_affidavit_Var.set(0)
                    self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_gray)
                elif self.pending_data[4] == 1:
                    self.purchaser_affidavit_Var.set(1)
                    self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_green)
                elif self.pending_data[4] == 2:
                    self.purchaser_affidavit_Var.set(2)
                    self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_red)
            elif self.pending_data[4] == 0:
                self.purchaser_affidavit_Var.set(0)
                self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_gray)

            self.self_decla_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\self_decla_gray.png"))
            self.self_decla_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\self_decla_green.png"))
            self.self_decla_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\self_decla_red.png"))
            self.self_declaration_Var = IntVar()
            self.self_declaration_chk_box = Button(self.pending_root, textvariable=self.self_declaration_Var,
                                                   image=self.self_decla_gray,
                                                   bg="#B39CD0",
                                                   activebackground="#B39CD0",
                                                   borderwidth=0,
                                                   command=self.self_decla_change,
                                                   )
            self.self_declaration_chk_box.place(x=502, y=110)
            if self.pending_data == []:
                self.self_declaration_chk_box.config(image=self.self_decla_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[5] == 0:
                    self.self_declaration_Var.set(0)
                    self.self_declaration_chk_box.config(image=self.self_decla_gray)
                elif self.pending_data[5] == 1:
                    self.self_declaration_Var.set(1)
                    self.self_declaration_chk_box.config(image=self.self_decla_green)
                elif self.pending_data[5] == 2:
                    self.self_declaration_Var.set(2)
                    self.self_declaration_chk_box.config(image=self.self_decla_red)
            elif self.pending_data[5] == 0:
                self.self_declaration_Var.set(0)
                self.self_declaration_chk_box.config(image=self.self_decla_gray)




            self.seller_id_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\seller_id_gray.png"))
            self.seller_id_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\seller_id_green.png"))
            self.seller_id_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\seller_id_red.png"))
            self.seller_id_Var = IntVar()
            self.seller_id_chk_box = Button(self.pending_root, textvariable=self.seller_id_Var,
                                            image=self.seller_id_gray,
                                            bg="#B39CD0",
                                            activebackground="#B39CD0",
                                            borderwidth=0,
                                            command=self.seller_id_change,
                                            )
            self.seller_id_chk_box.place(x=16, y=148)
            if self.pending_data == []:
                self.seller_id_chk_box.config(image=self.seller_id_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[6] == 0:
                    self.seller_id_Var.set(0)
                    self.seller_id_chk_box.config(image=self.seller_id_gray)
                elif self.pending_data[6] == 1:
                    self.seller_id_Var.set(1)
                    self.seller_id_chk_box.config(image=self.seller_id_green)
                elif self.pending_data[6] == 2:
                    self.seller_id_Var.set(2)
                    self.seller_id_chk_box.config(image=self.seller_id_red)
            elif self.pending_data[6] == 0:
                self.seller_id_Var.set(0)
                self.seller_id_chk_box.config(image=self.seller_id_gray)




            self.purchaser_id_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\purchaser_id_gray.png"))
            self.purchaser_id_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\purchaser_id_green.png"))
            self.purchaser_id_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\purchaser_id_red.png"))
            self.purchaser_id_Var = IntVar()
            self.purchaser_id_chk_box = Button(self.pending_root, textvariable=self.purchaser_id_Var,
                                               image=self.purchaser_id_gray,
                                               bg="#B39CD0",
                                               activebackground="#B39CD0",
                                               borderwidth=0,
                                               command=self.purchaser_id_change,
                                               )
            self.purchaser_id_chk_box.place(x=259, y=148)
            if self.pending_data == []:
                self.purchaser_id_chk_box.config(image=self.purchaser_id_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[7] == 0:
                    self.purchaser_id_Var.set(0)
                    self.purchaser_id_chk_box.config(image=self.purchaser_id_gray)
                elif self.pending_data[7] == 1:
                    self.purchaser_id_Var.set(1)
                    self.purchaser_id_chk_box.config(image=self.purchaser_id_green)
                elif self.pending_data[7] == 2:
                    self.purchaser_id_Var.set(2)
                    self.purchaser_id_chk_box.config(image=self.purchaser_id_red)
            elif self.pending_data[7] == 0:
                self.purchaser_id_Var.set(0)
                self.purchaser_id_chk_box.config(image=self.purchaser_id_gray)





            self.passport_size_photo_gray = ImageTk.PhotoImage(
                Image.open(r"images\pending_doc\passport_size_photo_gray.png"))
            self.passport_size_photo_green = ImageTk.PhotoImage(
                Image.open(r"images\pending_doc\passport_size_photo_green.png"))
            self.passport_size_photo_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\passport_size_photo_red.png"))
            self.passport_size_photo_Var = IntVar()
            self.passport_size_chk_box = Button(self.pending_root, textvariable=self.passport_size_photo_Var,
                                                image=self.passport_size_photo_gray,
                                                bg="#B39CD0",
                                                activebackground="#B39CD0",
                                                borderwidth=0,
                                                command=self.passport_size_photo_change,
                                                )
            self.passport_size_chk_box.place(x=502, y=148)
            if self.pending_data == []:
                self.passport_size_chk_box.config(image=self.passport_size_photo_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[8] == 0:
                    self.passport_size_photo_Var.set(0)
                    self.passport_size_chk_box.config(image=self.passport_size_photo_gray)
                elif self.pending_data[8] == 1:
                    self.passport_size_photo_Var.set(1)
                    self.passport_size_chk_box.config(image=self.passport_size_photo_green)
                elif self.pending_data[8] == 2:
                    self.passport_size_photo_Var.set(2)
                    self.passport_size_chk_box.config(image=self.passport_size_photo_red)
            elif self.pending_data[8] == 0:
                self.passport_size_photo_Var.set(0)
                self.passport_size_chk_box.config(image=self.passport_size_photo_gray)




            self.vehicle_photos_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\vehicle_photos_gray.png"))
            self.vehicle_photos_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\vehicle_photos_green.png"))
            self.vehicle_photos_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\vehicle_photos_red.png"))
            self.vehicle_photo_Var = IntVar()
            self.vehicle_photo_chk_box = Button(self.pending_root, textvariable=self.vehicle_photo_Var,
                                                image=self.vehicle_photos_gray,
                                                bg="#B39CD0",
                                                activebackground="#B39CD0",
                                                borderwidth=0,
                                                command=self.vehicle_photos_change,
                                                )
            self.vehicle_photo_chk_box.place(x=16, y=186)
            if self.pending_data == []:
                self.vehicle_photo_chk_box.config(image=self.vehicle_photos_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[9] == 0:
                    self.vehicle_photo_Var.set(0)
                    self.vehicle_photo_chk_box.config(image=self.vehicle_photos_gray)
                elif self.pending_data[9] == 1:
                    self.vehicle_photo_Var.set(1)
                    self.vehicle_photo_chk_box.config(image=self.vehicle_photos_green)
                elif self.pending_data[9] == 2:
                    self.vehicle_photo_Var.set(2)
                    self.vehicle_photo_chk_box.config(image=self.vehicle_photos_red)
            elif self.pending_data[9] == 0:
                self.vehicle_photo_Var.set(0)
                self.vehicle_photo_chk_box.config(image=self.vehicle_photos_gray)




            self.vehicle_insurance_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\vehicle_insurance_gray.png"))
            self.vehicle_insurance_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\vehicle_insurance_green.png"))
            self.vehicle_insurance_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\vehicle_insurance_red.png"))
            self.vehicle_insurance_Var = IntVar()
            self.vehicle_insurance_chk_box = Button(self.pending_root, textvariable=self.vehicle_insurance_Var,
                                                    image=self.vehicle_insurance_gray,
                                                    bg="#B39CD0",
                                                    activebackground="#B39CD0",
                                                    borderwidth=0,
                                                    command=self.vehicle_insurance_change,
                                                    )
            self.vehicle_insurance_chk_box.place(x=259, y=186)
            if self.pending_data == []:
                self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[10] == 0:
                    self.vehicle_insurance_Var.set(0)
                    self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_gray)
                elif self.pending_data[10] == 1:
                    self.vehicle_insurance_Var.set(1)
                    self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_green)
                elif self.pending_data[10] == 2:
                    self.vehicle_insurance_Var.set(2)
                    self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_red)
            elif self.pending_data[10] == 0:
                self.vehicle_insurance_Var.set(0)
                self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_gray)

            self.pollution_gray = ImageTk.PhotoImage(Image.open(r"images\pending_doc\pollution_gray.png"))
            self.pollution_green = ImageTk.PhotoImage(Image.open(r"images\pending_doc\pollution_green.png"))
            self.pollution_red = ImageTk.PhotoImage(Image.open(r"images\pending_doc\pollution_red.png"))
            self.pollution_Var1 = IntVar()
            self.pollution_chk_box1 = Button(self.pending_root, textvariable=self.pollution_Var1,
                                            image=self.pollution_gray,
                                            bg="#B39CD0",
                                            activebackground="#B39CD0",
                                            borderwidth=0,
                                            command=self.pollution_change,
                                            )
            self.pollution_chk_box1.place(x=502, y=186)
            if self.pending_data == []:
                self.pollution_chk_box1.config(image=self.pollution_gray)
            elif len(self.pending_data) == 12:
                if self.pending_data[11] == 0:
                    self.pollution_Var1.set(0)
                    self.pollution_chk_box1.config(image=self.pollution_gray)
                elif self.pending_data[11] == 1:
                    self.pollution_Var1.set(1)
                    self.pollution_chk_box1.config(image=self.pollution_green)
                elif self.pending_data[11] == 2:
                    self.pollution_Var1.set(2)
                    self.pollution_chk_box1.config(image=self.pollution_red)
            elif self.pending_data[11] == 0:
                self.pollution_Var1.set(0)
                self.pollution_chk_box1.config(image=self.pollution_gray)

            self.submit_btn_img1 = ImageTk.PhotoImage(Image.open(r"images\submit_btn_img.png"))

            self.submit_data_btn1 = Button(self.pending_root,
                                           image=self.submit_btn_img1,
                                           borderwidth=0,
                                           width=150,
                                           height=35,
                                           relief=FLAT,
                                           command=self.pending_submit_fun)

            self.submit_data_btn1.place(x=270, y=400)

            # Label(text="OTHERS", font=("Helvetica", "12")).place(x=220, y=410)
            # self.name_var = StringVar()
            # self.name_entry = Entry(textvariable=self.name_var, bg="#D9D9D9", border=0, font=("Helvetica", "12"))
            # self.name_entry.place(x=300, y=410)

            self.pending_root.mainloop()

    def on_close_pending_window(self):
        self.pending_window = False
        self.pending_root.destroy()

    def pb_permit_change(self):

        if self.pb_permit_new_Var1.get() == 2:
            self.pb_permit_new_chk_box1.config(image=self.pb_new_gray)
            self.pb_permit_new_Var1.set(0)
            print("______________________")
            print(self.pb_permit_new_Var1.get())

        elif self.pb_permit_new_Var1.get() == 0:
            self.pb_permit_new_chk_box1.config(image=self.pb_new_green)
            self.pb_permit_new_Var1.set(1)
            print("======================")
            print(self.pb_permit_new_Var1.get())

        elif self.pb_permit_new_Var1.get() == 1:
            self.pb_permit_new_chk_box1.config(image=self.pb_new_red)
            self.pb_permit_new_Var1.set(2)
            print("*********************")
            print(self.pb_permit_new_Var1.get())

    def np_permit_change(self):
        if self.np_permit_Var1.get() == 2:
            self.np_permit_chk_box1.config(image=self.np_permit_gray)
            self.np_permit_Var1.set(0)
            print(self.np_permit_Var1.get())
        elif self.np_permit_Var1.get() == 0:
            self.np_permit_chk_box1.config(image=self.np_permit_green)
            self.np_permit_Var1.set(1)
            print(self.np_permit_Var1.get())
        elif self.np_permit_Var1.get() == 1:
            self.np_permit_chk_box1.config(image=self.np_permit_red)
            self.np_permit_Var1.set(2)
            print(self.np_permit_Var1.get())

    def bank_noc_change(self):
        if self.bank_noc_Var1.get() == 2:
            self.bank_noc_chk_box1.config(image=self.bank_noc_gray)
            self.bank_noc_Var1.set(0)
            print(self.bank_noc_Var1.get())
        elif self.bank_noc_Var1.get() == 0:
            self.bank_noc_chk_box1.config(image=self.bank_noc_green)
            self.bank_noc_Var1.set(1)
            print(self.bank_noc_Var1.get())
        elif self.bank_noc_Var1.get() == 1:
            self.bank_noc_chk_box1.config(image=self.bank_noc_red)
            self.bank_noc_Var1.set(2)
            print(self.bank_noc_Var1.get())

    def seller_aff_change(self):
        if self.seller_affidavit_Var.get() == 2:
            self.seller_affidavit_chk_box.config(image=self.seller_aff_gray)
            self.seller_affidavit_Var.set(0)
            print(self.seller_affidavit_Var.get())
        elif self.seller_affidavit_Var.get() == 0:
            self.seller_affidavit_chk_box.config(image=self.seller_aff_green)
            self.seller_affidavit_Var.set(1)
            print(self.seller_affidavit_Var.get())
        elif self.seller_affidavit_Var.get() == 1:
            self.seller_affidavit_chk_box.config(image=self.seller_aff_red)
            self.seller_affidavit_Var.set(2)
            print(self.seller_affidavit_Var.get())

    def purchaser_aff_change(self):
        if self.purchaser_affidavit_Var.get() == 2:
            self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_gray)
            self.purchaser_affidavit_Var.set(0)
            print(self.purchaser_affidavit_Var.get())
        elif self.purchaser_affidavit_Var.get() == 0:
            self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_green)
            self.purchaser_affidavit_Var.set(1)
            print(self.purchaser_affidavit_Var.get())
        elif self.purchaser_affidavit_Var.get() == 1:
            self.purchaser_affidavit_chk_box.config(image=self.purchaser_aff_red)
            self.purchaser_affidavit_Var.set(2)
            print(self.purchaser_affidavit_Var.get())

    def self_decla_change(self):
        if self.self_declaration_Var.get() == 2:
            self.self_declaration_chk_box.config(image=self.self_decla_gray)
            self.self_declaration_Var.set(0)
            print(self.self_declaration_Var.get())
        elif self.self_declaration_Var.get() == 0:
            self.self_declaration_chk_box.config(image=self.self_decla_green)
            self.self_declaration_Var.set(1)
            print(self.self_declaration_Var.get())
        elif self.self_declaration_Var.get() == 1:
            self.self_declaration_chk_box.config(image=self.self_decla_red)
            self.self_declaration_Var.set(2)
            print(self.self_declaration_Var.get())

    def seller_id_change(self):
        if self.seller_id_Var.get() == 2:
            self.seller_id_chk_box.config(image=self.seller_id_gray)
            self.seller_id_Var.set(0)
            print(self.seller_id_Var.get())
        elif self.seller_id_Var.get() == 0:
            self.seller_id_chk_box.config(image=self.seller_id_green)
            self.seller_id_Var.set(1)
            print(self.seller_id_Var.get())
        elif self.seller_id_Var.get() == 1:
            self.seller_id_chk_box.config(image=self.seller_id_red)
            self.seller_id_Var.set(2)
            print(self.seller_id_Var.get())

    def purchaser_id_change(self):
        if self.purchaser_id_Var.get() == 2:
            self.purchaser_id_chk_box.config(image=self.purchaser_id_gray)
            self.purchaser_id_Var.set(0)
            print(self.purchaser_id_Var.get())
        elif self.purchaser_id_Var.get() == 0:
            self.purchaser_id_chk_box.config(image=self.purchaser_id_green)
            self.purchaser_id_Var.set(1)
            print(self.purchaser_id_Var.get())
        elif self.purchaser_id_Var.get() == 1:
            self.purchaser_id_chk_box.config(image=self.purchaser_id_red)
            self.purchaser_id_Var.set(2)
            print(self.purchaser_id_Var.get())

    def passport_size_photo_change(self):
        if self.passport_size_photo_Var.get() == 2:
            self.passport_size_chk_box.config(image=self.passport_size_photo_gray)
            self.passport_size_photo_Var.set(0)
            print(self.passport_size_photo_Var.get())
        elif self.passport_size_photo_Var.get() == 0:
            self.passport_size_chk_box.config(image=self.passport_size_photo_green)
            self.passport_size_photo_Var.set(1)
            print(self.passport_size_photo_Var.get())
        elif self.passport_size_photo_Var.get() == 1:
            self.passport_size_chk_box.config(image=self.passport_size_photo_red)
            self.passport_size_photo_Var.set(2)
            print(self.passport_size_photo_Var.get())

    def vehicle_photos_change(self):
        if self.vehicle_photo_Var.get() == 2:
            self.vehicle_photo_chk_box.config(image=self.vehicle_photos_gray)
            self.vehicle_photo_Var.set(0)
            print(self.vehicle_photo_Var.get())
        elif self.vehicle_photo_Var.get() == 0:
            self.vehicle_photo_chk_box.config(image=self.vehicle_photos_green)
            self.vehicle_photo_Var.set(1)
            print(self.vehicle_photo_Var.get())
        elif self.vehicle_photo_Var.get() == 1:
            self.vehicle_photo_chk_box.config(image=self.vehicle_photos_red)
            self.vehicle_photo_Var.set(2)
            print(self.vehicle_photo_Var.get())

    def vehicle_insurance_change(self):
        if self.vehicle_insurance_Var.get() == 2:
            self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_gray)
            self.vehicle_insurance_Var.set(0)
            print(self.vehicle_insurance_Var.get())
        elif self.vehicle_insurance_Var.get() == 0:
            self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_green)
            self.vehicle_insurance_Var.set(1)
            print(self.vehicle_insurance_Var.get())
        elif self.vehicle_insurance_Var.get() == 1:
            self.vehicle_insurance_chk_box.config(image=self.vehicle_insurance_red)
            self.vehicle_insurance_Var.set(2)
            print(self.vehicle_insurance_Var.get())

    def pollution_change(self):
        if self.pollution_Var1.get() == 2:
            self.pollution_chk_box1.config(image=self.pollution_gray)
            self.pollution_Var1.set(0)
            print(self.pollution_Var1.get())
        elif self.pollution_Var1.get() == 0:
            self.pollution_chk_box1.config(image=self.pollution_green)
            self.pollution_Var1.set(1)
            print(self.pollution_Var1.get())
        elif self.pollution_Var1.get() == 1:
            self.pollution_chk_box1.config(image=self.pollution_red)
            self.pollution_Var1.set(2)
            print(self.pollution_Var1.get())

    def pending_submit_fun(self):
        if check_internet.check_internet():
            # print(f"pb_permit_new_Var :{self.pb_permit_new_Var1.get()}")
            # print(f"np_permit_Var :{self.np_permit_Var1.get()}")
            # print(f"bank_noc_Var :{self.bank_noc_Var1.get()}")
            # print(f"seller_affidavit_Var :{self.seller_affidavit_Var.get()}")
            # print(f"purchaser_affidavit_Var :{self.purchaser_affidavit_Var.get()}")
            # print(f"self_declaration_Var :{self.self_declaration_Var.get()}")
            # print(f"seller_id_Var :{self.seller_id_Var.get()}")
            # print(f"purchaser_id_Var :{self.purchaser_id_Var.get()}")
            # print(f"passport_size_photo_Var :{self.passport_size_photo_Var.get()}")
            # print(f"vehicle_photo_Var :{self.vehicle_photo_Var.get()}")
            # print(f"vehicle_insurance_Var :{self.vehicle_insurance_Var.get()}")
            # print(f"pollution_Var :{self.pollution_Var1.get()}")
            self.data[0]["pending_document"] = [self.pb_permit_new_Var1.get(),
                                                     self.np_permit_Var1.get(),
                                                     self.bank_noc_Var1.get(),
                                                     self.seller_affidavit_Var.get(),
                                                     self.purchaser_affidavit_Var.get(),
                                                     self.self_declaration_Var.get(),
                                                     self.seller_id_Var.get(),
                                                     self.purchaser_id_Var.get(),
                                                     self.passport_size_photo_Var.get(),
                                                     self.vehicle_photo_Var.get(),
                                                     self.vehicle_insurance_Var.get(),
                                                     self.pollution_Var1.get(),
                                                     ]
            # res = database.com_update_pending_doc(self.data)
            res = database.run_with_timeout(database.com_update_pending_doc, args=(self.data,),
                                            timeout=10)
            print(res)
            if res:
                self.pending_data = self.data[0]["pending_document"]
                self.update_data(self.all_data, self.data[0])
                print(self.data[0]["pending_document"])
                # messagebox.showinfo("Selection Successfull","")
                self.pending_window = False
                self.pending_root.destroy()
            else:
                messagebox.showwarning("connection error", "Please check your internet connection!",
                                   parent=self.pending_root)
        else:
            messagebox.showwarning("connection error", "Please check your internet connection!",
                                   parent=self.pending_root)










    def current_date_fun(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d-%m-%Y")
        return formatted_date


    def current_time_fun(self):
        current_time = datetime.now().time()
        formatted_time = current_time.strftime("%I:%M:%S %p")
        return formatted_time

if __name__ == '__main__':
    obj = Main()
    obj.window()
