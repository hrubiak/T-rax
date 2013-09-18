import scipy
import numpy as np
import T_Rax_Data as TRData
import T_Rax_Main_View as TRMView
from T_Rax_ROI_selector import TRaxROIController
import wx
from wx.lib.pubsub import Publisher as pub
import os


class TraxMainViewController(object):
    def __init__(self):
        self.data=TRData.TraxData()
        self.main_view = TRMView.TraxMainWindow(self)
        self.exp_controls = self.main_view.exp_panel
        self.timer = wx.Timer (self.main_view)
        self.calib_controls = self.main_view.calib_panel
        self._exp_working_dir=os.getcwd()
        self._calib_working_dir=os.getcwd()
        self.set_bindings()
        pub.sendMessage("EXP DATA CHANGED")

    def set_parameter(self):
        ds_txt_roi = self.data.roi_data.ds_roi.get_list()
        ds_txt_roi[2:] = self.data.calculate_wavelength(ds_txt_roi[2:])
        self.exp_controls.set_fit_x_limits(ds_txt_roi[2:])

    def set_bindings(self):
        self.exp_controls.exp_load_data_btn.Bind(wx.EVT_BUTTON, self.load_exp_data)
        self.exp_controls.exp_next_btn.Bind(wx.EVT_BUTTON, self.load_exp_next_data)
        self.exp_controls.exp_previous_btn.Bind(wx.EVT_BUTTON, self.load_exp_previous_data)

        self.exp_controls.exp_auto_process_cb.Bind(wx.EVT_CHECKBOX, self.auto_process_cb_click)
        self.main_view.Bind(wx.EVT_TIMER, self.check_files, self.timer)

        self.exp_controls.roi_setup_btn.Bind(wx.EVT_BUTTON, self.roi_setup_btn_click)
        pub.subscribe(self.data_changed, "EXP DATA CHANGED")
        pub.subscribe(self.roi_changed, "ROI CHANGED")
        self.main_view.Bind(wx.EVT_CLOSE, self.close_window_click)

        self.calib_controls.ds_calib_box.load_data_btn.Bind(wx.EVT_BUTTON, self.load_ds_calib_data)
        self.calib_controls.us_calib_box.load_data_btn.Bind(wx.EVT_BUTTON, self.load_us_calib_data)

        self.calib_controls.ds_calib_box.temperature_txt.Bind(wx.EVT_TEXT_ENTER, self.set_ds_temp)
        self.calib_controls.us_calib_box.temperature_txt.Bind(wx.EVT_TEXT_ENTER, self.set_us_temp)

        self.calib_controls.ds_calib_box.known_temperature_rb.Bind(wx.EVT_RADIOBUTTON, self.set_ds_modus_temp)
        self.calib_controls.ds_calib_box.etalon_spectrum_rb.Bind(wx.EVT_RADIOBUTTON, self.set_ds_modus_etalon)
        self.calib_controls.ds_calib_box.load_etalon_data_btn.Bind(wx.EVT_BUTTON, self.load_ds_etalon_data)

        self.calib_controls.us_calib_box.known_temperature_rb.Bind(wx.EVT_RADIOBUTTON, self.set_us_modus_temp)
        self.calib_controls.us_calib_box.etalon_spectrum_rb.Bind(wx.EVT_RADIOBUTTON, self.set_us_modus_etalon)
        self.calib_controls.us_calib_box.load_etalon_data_btn.Bind(wx.EVT_BUTTON, self.load_us_etalon_data)

        self.exp_controls.fit_from_txt.Bind(wx.EVT_TEXT_ENTER, self.fit_limits_txt_changed)
        self.exp_controls.fit_to_txt.Bind(wx.EVT_TEXT_ENTER, self.fit_limits_txt_changed)


    def load_exp_data(self, e):
        dlg = wx.FileDialog(self.main_view, message="Load Experiment SPE", 
                            defaultDir = self._exp_working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  
            self._exp_working_dir=os.path.split(path)[0]   
            self._files_before= dict([(f, None) for f in os.listdir(self._exp_working_dir)]) #reset for the autoprocessing  
            self.data.load_exp_data(path)
            self.set_parameter()

    def load_exp_next_data(self, e):
        self.data.load_next_exp_file()

    def load_exp_previous_data(self, e):
        self.data.load_previous_exp_file()

    def auto_process_cb_click(self, e):
        if e.EventObject.Value:
            self._files_before= dict([(f, None) for f in os.listdir(self._exp_working_dir)])
            self.timer.Start(100)
        else:
            self.timer.Stop()

    def check_files(self, event):
        self._files_now = dict([(f,None) for f in os.listdir (self._exp_working_dir)])
        self._files_added = [f for f in self._files_now if not f in self._files_before]
        self._files_removed = [f for f in self._files_before if not f in self._files_now]
        if len(self._files_added)>0:
            new_file_str=self._files_added[-1]
            if new_file_str.endswith('.SPE') or \
                    new_file_str.endswith('.spe'):
                path=self._exp_working_dir+'\\'+new_file_str
                self.data.load_exp_data(path)
            self._files_before=self._files_now
            
    def roi_setup_btn_click(self, event):
        try:
            self.roi_view = TRaxROIController(None, self.data)
        except TRaxROIController, s:
            s.activate()
        except wx._core.PyDeadObjectError:
            pass

    def fit_limits_txt_changed(self, event):
        new_limits = self.main_view.exp_panel.get_fit_x_limits()
        new_limits_ind=np.array(self.data.calculate_ind(new_limits))
        self.data.roi_data.set_x_limits(new_limits_ind)
        try:
            self.roi_view.view.graph_panel.update_line_limits()
            self.roi_view.view.graph_panel.update_lines()
        except:
            pass

    def load_ds_calib_data(self, event):
        dlg = wx.FileDialog(self.main_view, message="Load Downstream calibration SPE", 
                            defaultDir = self._calib_working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  
            self._calib_working_dir=os.path.split(path)[0]     
            self.data.load_ds_calib_data(path)

    def load_us_calib_data(self, event):
        dlg = wx.FileDialog(self.main_view, message="Load Upstream calibration SPE", 
                            defaultDir = self._calib_working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  
            self._calib_working_dir=os.path.split(path)[0]     
            self.data.load_us_calib_data(path)

    def set_us_temp(self, event):
        self.data.set_us_calib_temp(int(self.calib_controls.us_calib_box.temperature_txt.GetLabel()))

    def set_ds_temp(self, event):
        self.data.set_ds_calib_temp(int(self.calib_controls.ds_calib_box.temperature_txt.GetLabel()))

    def set_ds_modus_temp(self, event):
        self.data.set_ds_calib_modus(0)

    def set_us_modus_temp(self, event):
        self.data.set_us_calib_modus(0)

    def set_ds_modus_etalon(self, event):
        if self.data.ds_calib_param.etalon_spectrum_func==None:
            self.main_view.calib_panel.ds_calib_box.known_temperature_rb.SetValue(True)
            self.data.set_ds_calib_modus(0)
        else:
            self.data.set_ds_calib_modus(1)

    def set_us_modus_etalon(self, event):
        if self.data.us_calib_param.etalon_spectrum_func==None:
            self.main_view.calib_panel.us_calib_box.known_temperature_rb.SetValue(True)
            self.data.set_us_calib_modus(0)
        else:
            self.data.set_us_calib_modus(1)

    def load_ds_etalon_data(self, event):
        dlg = wx.FileDialog(self.main_view, message="Load Downstream Etalon spectrum", 
                            defaultDir = self._calib_working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()     
            self.data.load_ds_calib_etalon(path)
            self.calib_controls.ds_calib_box.etalon_file_lbl.SetLabel(path.split('\\')[-1])

    def load_us_etalon_data(self, event):
        dlg = wx.FileDialog(self.main_view, message="Load Upstream Etalon spectrum", 
                            defaultDir = self._calib_working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()     
            self.data.load_us_calib_etalon(path)
            self.calib_controls.us_calib_box.etalon_file_lbl.SetLabel(path.split('\\')[-1])

    def data_changed(self, message):
        self.main_view.graph_panel.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.exp_controls.exp_file_lbl.SetLabel(self.data.get_exp_file_name().split('\\')[-1])
        self.calib_controls.ds_calib_box.file_lbl.SetLabel(self.data.get_ds_calib_file_name().split('\\')[-1])
        self.calib_controls.us_calib_box.file_lbl.SetLabel(self.data.get_us_calib_file_name().split('\\')[-1])
        self.calib_controls.ds_calib_box.etalon_file_lbl.SetLabel(self.data.get_ds_calib_etalon_file_name().split('\\')[-1])
        self.calib_controls.us_calib_box.etalon_file_lbl.SetLabel(self.data.get_us_calib_etalon_file_name().split('\\')[-1])
        self.set_parameter()

    def roi_changed(self, message):
        self.main_view.graph_panel.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        ds_txt_roi = self.data.roi_data.ds_roi.get_list()
        ds_txt_roi[2:] = self.data.calculate_wavelength(ds_txt_roi[2:])
        self.main_view.exp_panel.set_fit_x_limits(ds_txt_roi[2:])

    def close_window_click(self, event):
        try:
            self.roi_view.view.Destroy()
            del self.roi_view
        except:
            pass
        self.main_view.Destroy()
        self.data.save_roi_data()

if __name__=="__main__":
    app=wx.App(None)
    main_view=TraxMainViewController()
   # main_view.data.load_exp_data('spe files\\Pt_38.SPE')
    #main_view.data.load_exp_data('SPE test vers3\\test_075.spe')
    
    main_view.data.load_exp_data('binary files\\lamp_15_dn.SPE')
    #main_view.data.load_ds_calib_data('binary files\\lamp_15_dn.SPE')
    #main_view.data.load_us_calib_data('binary files\\lamp_15_up.SPE')
    app.MainLoop()

