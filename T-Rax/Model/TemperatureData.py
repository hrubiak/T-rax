import random

from wx.lib.pubsub import pub
import numpy as np
from scipy.optimize import curve_fit

from model.SpeFile import SpeFile
from model.GeneralData import GeneralData


class TemperatureData(GeneralData):
    def __init__(self):
        super(TemperatureData, self).__init__()
        self.ds_calibration_data = None
        self.us_calibration_data = None
        self.ds_calibration_parameter = CalibrationParameter()
        self.us_calibration_parameter = CalibrationParameter()

        try:
            self.get_us_calibration_parameter().load_etalon_spectrum('15A_lamp.txt')
            self.get_ds_calibration_parameter().load_etalon_spectrum('15A_lamp.txt')
        except IOError:
            self.ds_calibration_parameter.set_modus(0)
            self.us_calibration_parameter.set_modus(0)

        self.roi_data_manager = RoiDataManager()
        self.exp_data = DummyImg(self.roi_data_manager)
        self.roi_data = self.exp_data.roi_data

        pub.sendMessage("EXP DATA CHANGED")
        pub.sendMessage("ROI CHANGED")

    def _read_exp_image_file(self, filename):
        img_file = SpeFile(filename)
        return ExpData(img_file, self.roi_data_manager)

    def load_exp_file(self, filename):
        self.file_name_iterator.update_filename(filename)

        self.exp_data = self._read_exp_image_file(filename)
        self.roi_data = self.exp_data.roi_data
        try:
            self.ds_calibration_data.roi_data = self.roi_data
        except AttributeError:
            pass
        try:
            self.us_calibration_data.roi_data = self.roi_data
        except AttributeError:
            pass
        self.calculate_spectra()
        pub.sendMessage("EXP DATA CHANGED")

    def load_ds_calibration_data(self, filename, send_message=True):
        self.ds_calibration_data = self._read_exp_image_file(filename)
        self.calculate_spectra()
        if send_message:
            pub.sendMessage("EXP DATA CHANGED")

    def load_us_calibration_data(self, filename, send_message=True):
        self.us_calibration_data = self._read_exp_image_file(filename)
        self.calculate_spectra()
        if send_message:
            pub.sendMessage("EXP DATA CHANGED")

    def calculate_spectra(self):
        self.exp_data.calc_spectra()
        if self.ds_calibration_data is not None:
            self.ds_calibration_data.calc_spectra()
        if self.us_calibration_data is not None:
            self.us_calibration_data.calc_spectra()

    def get_ds_spectrum(self):
        try:
            if self.exp_data.get_img_dimension() == self.ds_calibration_data.get_img_dimension():
                x = self.exp_data.ds_spectrum.x
                corrected_spectrum = self.exp_data.calc_corrected_ds_spectrum(self.ds_calibration_data.ds_spectrum,
                                                                              self.ds_calibration_parameter.
                                                                              get_calibration_y(x))
                self.ds_fitted_spectrum = FitSpectrum(corrected_spectrum)
                return [corrected_spectrum, self.ds_fitted_spectrum]
            else:
                return self.exp_data.ds_spectrum
        except AttributeError:
            return self.exp_data.ds_spectrum

    def get_us_spectrum(self):
        try:
            if self.exp_data.get_img_dimension() == self.us_calibration_data.get_img_dimension():
                x = self.exp_data.us_spectrum.x
                corrected_spectrum = self.exp_data.calc_corrected_us_spectrum(self.us_calibration_data.us_spectrum,
                                                                              self.us_calibration_parameter.get_calibration_y(
                                                                                  x))
                self.us_fitted_spectrum = FitSpectrum(corrected_spectrum)
                return [corrected_spectrum, self.us_fitted_spectrum]
            else:
                return self.exp_data.us_spectrum
        except AttributeError:
            return self.exp_data.us_spectrum

    def get_ds_temperature(self):
        try:
            return self.ds_fitted_spectrum.T
        except AttributeError:
            return 0

    def get_us_temperature(self):
        try:
            return self.us_fitted_spectrum.T
        except AttributeError:
            return 0

    def get_x_roi_limits(self):
        return self.get_wavelength_from(self.exp_data.roi_data.get_x_limits())

    def set_x_roi_limits_to(self, limits):
        limits_ind = self.get_index_from(limits)
        self.roi_data.set_x_limits(limits_ind)

    def get_roi_data(self):
        return self.roi_data

    def get_ds_calibration_data(self):
        return self.ds_calibration_data

    def get_us_calibration_data(self):
        return self.us_calibration_data

    def get_ds_calibration_parameter(self):
        return self.ds_calibration_parameter

    def get_us_calibration_parameter(self):
        return self.us_calibration_parameter

    def calculate_time_lapse(self):
        old_frame_number = self.exp_data.current_frame
        ds_temperature = []
        ds_temperature_err = []
        us_temperature = []
        us_temperature_err = []
        for frame_number in xrange(self.exp_data.num_frames):
            self.exp_data.current_frame = frame_number
            self.calculate_spectra()
            dummy, ds_fit = self.get_ds_spectrum()
            dummy, us_fit = self.get_us_spectrum()
            ds_temperature.append(ds_fit.T)
            us_temperature.append(us_fit.T)
            ds_temperature_err.append(ds_fit.T_err)
            us_temperature_err.append(us_fit.T_err)
            progress = np.int(np.round((float(frame_number + 1) / self.exp_data.num_frames) * 100))
            pub.sendMessage("PROGRESS ONGOING", progress=progress)

        self.exp_data.current_frame = old_frame_number
        return ds_temperature, ds_temperature_err, \
               us_temperature, us_temperature_err


class GeneralData(object):
    def __init__(self, img_file, roi_data_manager):
        self._img_file = img_file
        self.roi_data = roi_data_manager.get_roi_data(img_file.get_dimension())

        self.filename = self._img_file.filename
        self._img_data = self._img_file.img
        self.x_whole = self._img_file.x_calibration
        self.current_frame = 0
        self.num_frames = self._img_file.num_frames

        self.calc_spectra()

    def img_data(self):
        if self.num_frames > 1:
            return self._img_data[self.current_frame]
        else:
            return self._img_data

    def calc_spectra(self):
        raise NotImplementedError

    def get_ds_y(self):
        raise NotImplementedError

    def get_us_y(self):
        raise NotImplementedError

    def get_ds_spectrum(self):
        raise NotImplementedError

    def get_us_spectrum(self):
        raise NotImplementedError

    def get_img_dimension(self):
        return self._img_file.get_dimension()

    def get_exposure_time(self):
        return self._img_file.exposure_time

    def get_file_information(self):
        return ('{exp_time:g}s, ' +
                '{detector}, ' +
                '{grating}, ' +
                '{center_wavelength:g}nm').format(exp_time=self._img_file.exposure_time,
                                                  detector=self._img_file.detector,
                                                  grating=self._img_file.grating,
                                                  center_wavelength=self._img_file.center_wavelength)


class ImgData(GeneralData):
    def calc_spectra(self):
        x = self.x_whole[self.roi_data.us_roi.x_min:
        self.roi_data.us_roi.x_max + 1]
        self.ds_spectrum = Spectrum(x, self._calc_spectrum(self.roi_data.ds_roi))
        self.us_spectrum = Spectrum(x, self._calc_spectrum(self.roi_data.us_roi))

    def _calc_spectrum(self, roi):
        roi_img = self.get_roi_img(roi)
        return np.sum(roi_img, 0) / np.float(np.size(roi_img, 0))

    def get_ds_roi_max(self):
        return np.max(self.get_roi_img(self.roi_data.ds_roi))

    def get_us_roi_max(self):
        return np.max(self.get_roi_img(self.roi_data.us_roi))

    def get_ds_roi_img(self):
        return self.get_roi_img(self.roi_data.ds_roi)

    def get_us_roi_img(self):
        return self.get_roi_img(self.roi_data.us_roi)

    def get_roi_img(self, roi):
        return self.img_data()[roi.y_min: roi.y_max + 1, roi.x_min:roi.x_max + 1]

    def get_x_limits(self):
        return np.array([min(self.x_whole), max(self.x_whole)])

    def get_x_whole(self):
        return self.x_whole

    def get_ds_y(self):
        return self.ds_spectrum.y

    def get_us_y(self):
        return self.us_spectrum.y

    def get_ds_spectrum(self):
        return self.ds_spectrum

    def get_us_spectrum(self):
        return self.us_spectrum


class ExpData(ImgData):
    def __init__(self, img_file, roi_data_manager):
        super(ExpData, self).__init__(img_file, roi_data_manager)
        self._get_file_name_info()

    def get_img_data(self):
        return self.img_data()

    def calc_corrected_ds_spectrum(self, calib_img_spectrum, calib_spectrum):
        response_function = calib_img_spectrum.y / calib_spectrum
        response_function[np.where(response_function == 0)] = np.NaN
        corrected_exp_y = self.ds_spectrum.y / response_function
        corrected_exp_y = corrected_exp_y / max(corrected_exp_y) * max(self.ds_spectrum.y)
        self.ds_corrected_spectrum = Spectrum(self.ds_spectrum.x, corrected_exp_y)
        return self.ds_corrected_spectrum

    def calc_corrected_us_spectrum(self, calib_img_spectrum, calib_spectrum):
        response_function = calib_img_spectrum.y / calib_spectrum
        response_function[np.where(response_function == 0)] = np.NaN
        corrected_exp_y = self.us_spectrum.y / response_function
        corrected_exp_y = corrected_exp_y / max(corrected_exp_y) * max(self.us_spectrum.y)
        self.us_corrected_spectrum = Spectrum(self.us_spectrum.x, corrected_exp_y)
        test = FitSpectrum(self.us_corrected_spectrum)
        return self.us_corrected_spectrum

    def _get_file_name_info(self):
        file_str = ''.join(self.filename.split('.')[0:-1])
        self._file_type = self.filename.split('.')[-1]

        self._file_number_str = self._get_ending_number(file_str)
        try:
            self._file_number = int(self._file_number_str)
            self._file_base_str = file_str[:-len(self._file_number_str)]
        except ValueError:
            return -1

    def _get_ending_number(self, str):
        res = ''
        for char in reversed(str):
            if char.isdigit():
                res += char
            else:
                return res[::-1]

    def get_next_file_names(self):
        new_file_name = self._file_base_str + str(self._file_number + 1) + \
                        '.' + self._file_type
        format_str = '0' + str(len(self._file_number_str)) + 'd'
        number_str = ("{0:" + format_str + '}').format(self._file_number + 1)
        new_file_name_with_leading_zeros = self._file_base_str + \
                                           number_str + '.' + self._file_type
        return new_file_name, new_file_name_with_leading_zeros

    def get_previous_file_names(self):
        new_file_name = self._file_base_str + str(self._file_number - 1) + \
                        '.' + self._file_type
        format_str = '0' + str(len(self._file_number_str)) + 'd'
        number_str = ("{0:" + format_str + '}').format(self._file_number - 1)
        new_file_name_with_leading_zeros = self._file_base_str + \
                                           number_str + '.' + self._file_type
        return new_file_name, new_file_name_with_leading_zeros

    def set_current_frame(self, frame_number):
        if frame_number >= self.num_frames - 1:
            self.current_frame = self.num_frames - 1
        elif frame_number < 1:
            self.current_frame = 0
        else:
            self.current_frame = frame_number
        pub.sendMessage("EXP DATA FRAME CHANGED")

    def load_next_frame(self):
        self.set_current_frame(self.current_frame + 1)

    def load_previous_frame(self):
        self.set_current_frame(self.current_frame - 1)


class DummyImg(ExpData):
    def __init__(self, roi_data_manager):
        self.num_frames = 10
        self.current_frame = 0
        self.roi_data = roi_data_manager.get_roi_data([1300, 100])
        self.create_img()
        self.filename = 'dummy_img.spe'

    def create_img(self):
        x = np.linspace(645, 850, 1024)
        y = np.linspace(0, 101, 256)
        X, Y = np.meshgrid(x, y)

        Z = np.ones((len(y), len(x)))
        random.seed()
        self._img_data = []
        for frame_number in xrange(self.num_frames):
            T1 = random.randrange(1700, 3000, 1)
            T2 = T1 + random.randrange(-200, 200, 1)

            black1 = black_body_function(x, T1, 1e-8)
            gauss1 = gauss_curve_function(y, 2, 80, 3)
            black2 = black_body_function(x, T2, 1e-8)
            gauss2 = gauss_curve_function(y, 2, 15, 3)

            for x_ind in xrange(len(x)):
                for y_ind in xrange(len(y)):
                    Z[y_ind, x_ind] = black1[x_ind] * gauss1[y_ind] + black2[x_ind] * gauss2[y_ind]
            self._img_data.append(Z + np.random.normal(0, .1 * max(black1), (len(y), len(x))))
        self.x_whole = x
        self.calc_spectra()

    def get_next_file_names(self):
        return '', ''

    def get_previous_file_names(self):
        return '', ''

    def get_img_dimension(self):
        return (1300, 100)

    def get_file_information(self):
        return '10s, dummy spec, 550nm'


class ExpDataFromImgData(ExpData):
    def __init__(self, img_data, filename, x_calibration, roi_data_manager):
        self._img_data = img_data
        self.num_frames = 1
        self.filename = filename
        self.x_whole = x_calibration
        self.img_dimension = (np.size(self._img_data, 1), np.size(self._img_data, 0))
        self.roi_data = roi_data_manager.get_roi_data(self.get_img_dimension())
        self.calc_spectra()

    def get_img_dimension(self):
        return self.img_dimension


class CalibrationParameter(object):
    def __init__(self):
        self.modus = 1
        # modi: 0 - given temperature
        #       1 - etalon spectrum

        self.temp = 2000
        self.etalon_spectrum_func = None
        self.etalon_file_name = 'Select File...'

    def set_modus(self, val, send_message=True):
        self.modus = val
        if send_message:
            pub.sendMessage("EXP DATA CHANGED")

    def set_temperature(self, temp, send_message=True):
        self.temp = temp
        if send_message:
            pub.sendMessage("EXP DATA CHANGED")

    def load_etalon_spectrum(self, fname, send_message=True):
        try:
            data = np.loadtxt(fname, delimiter=',')
        except ValueError:
            try:
                data = np.loadtxt(fname, delimiter=' ')
            except ValueError:
                try:
                    data = np.loadtxt(fname, delimiter=';')
                except ValueError:
                    data = np.loadtxt(fname, delimiter='\t')
        self._etalon_x = data.T[0]
        self._etalon_y = data.T[1]
        # self.etalon_spectrum_func = ip.interp1d(Model.T[0], Model.T[1], 'cubic')
        # not used because scipy.interpolate is supported by pyinstaller...
        self.etalon_file_name = fname
        if send_message:
            pub.sendMessage("EXP DATA CHANGED")

    def get_calibration_y(self, wavelength):
        if self.modus == 0:
            y = black_body_function(wavelength, self.temp, 1)
            return y / max(y)
        elif self.modus == 1:
            try:
                # return self.etalon_spectrum_func(wavelength)
                # not used because scipy.interpolate is supported by pyinstaller...
                return np.interp(wavelength, self._etalon_x, self._etalon_y)
            except ValueError:
                pub.sendMessage("INTERPOLATION RANGE ERROR")
                return np.ones(np.size(wavelength))

    def get_etalon_filename(self):
        return self.etalon_file_name

    def set_etalon_filename(self, filename):
        self.etalon_file_name = filename

    def get_etalon_spectrum(self):
        return Spectrum(self._etalon_x, self._etalon_y)

    def set_etalon_function_from_spectrum(self, spectrum):
        try:
            self._etalon_x = spectrum.x
            self._etalon_y = spectrum.y
            # self.etalon_spectrum_func = ip.interp1d(spectrum.x, spectrum.y, 'cubic')
        except AttributeError:
            pass


class Spectrum():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_y_range(self):
        return max(self.y) - min(self.y)

    def get_x_range(self):
        return max(self.x) - min(self.x)

    def get_x_plot_limits(self):
        return [min(self.x), max(self.x)]

    def get_y_plot_limits(self, factor=0.05):
        return [min(self.y), max(self.y) + factor * self.get_y_range()]

    def get_data(self):
        return [self.x, self.y]


class FitSpectrum(Spectrum):
    def __init__(self, spectrum):
        self._orig_spectrum = spectrum
        try:
            param, cov = curve_fit(black_body_function, spectrum.x, spectrum.y, p0=[2000, 1e-11])
            self.T = param[0]
            self.T_err = np.sqrt(cov[0, 0])

            self.x = spectrum.x
            self.y = black_body_function(self.x, param[0], param[1])
        except (RuntimeError, TypeError):
            self.T = np.NaN
            self.T_err = np.NaN
            self.x = []
            self.y = []


class Roi():
    def __init__(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]

    def set_x_limit(self, xlimit):
        self.x_min = xlimit[0]
        self.x_max = xlimit[1]

    def set_y_limit(self, ylimit):
        self.y_max = ylimit[0]
        self.y_max = ylimit[1]

    def set_x_max(self, x_max):
        if self.x_max > x_max:
            self.x_max = x_max
        if self.x_min >= x_max:
            self.x_min = 0

    def set_y_max(self, y_max):
        if self.y_max > y_max:
            self.y_max = y_max
        if self.y_min >= y_max:
            self.y_min = y_max - 1

    def get_width(self):
        return self.x_max - self.x_min

    def get_height(self):
        return self.y_max - self.y_min

    def get_x_limits(self):
        return [self.x_min, self.x_max]

    def get_y_limits(self):
        return [self.y_min, self.y_max]

    def get_roi_as_list(self):
        return [self.x_min, self.x_max, self.y_min, self.y_max]

    def set_roi(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]


class RoiDataManager():
    def __init__(self):
        self._img_dimensions_list = []
        self._roi_data_list = []
        self._num = 0
        self._current = None

    def _exists(self, dimension):
        if self._get_dimension_ind(dimension) is not None:
            return True
        else:
            return False

    def _add(self, img_dimension, roi_data):
        if self._exists(img_dimension):
            ind = self._get_dimension_ind(img_dimension)
            self._roi_data_list[ind] = roi_data
        else:
            self._img_dimensions_list.append(img_dimension)
            self._roi_data_list.append(roi_data)
            self._num += 1

    def _get_dimension_ind(self, img_dimension):
        for ind in range(self._num):
            if self._img_dimensions_list[ind] == img_dimension:
                self._current = ind
                return ind
        self._current = None
        return None

    def get_roi_data(self, img_dimension):
        if self._exists(img_dimension):
            return self._roi_data_list[self._get_dimension_ind(img_dimension)]
        else:
            ds_limits = np.array([0.25 * (img_dimension[0] - 1), 0.75 * (img_dimension[0] - 1),
                                  0.8 * (img_dimension[1] - 1), 0.9 * (img_dimension[1] - 1)])
            us_limits = np.array([0.25 * (img_dimension[0] - 1), 0.75 * (img_dimension[0] - 1),
                                  0.1 * (img_dimension[1] - 1), 0.2 * (img_dimension[1] - 1)])
            ds_limits = np.round(ds_limits)
            us_limits = np.round(us_limits)

            self._add(img_dimension, RoiData(ds_limits, us_limits))
            return self._roi_data_list[self._get_dimension_ind(img_dimension)]

    def get_current_roi(self):
        return self._roi_data_list[self._current]


class RoiData():
    def __init__(self, ds_limits, us_limits):
        self.ds_roi = Roi(ds_limits)
        self.us_roi = Roi(us_limits)

    def get_roi_data(self):
        data = [self.ds_roi.get_roi_as_list(), self.us_roi.get_roi_as_list()]
        return data

    def get_ds_roi(self):
        return self.ds_roi.get_roi_as_list()

    def get_us_roi(self):
        return self.us_roi.get_roi_as_list()

    def set_ds_roi(self, ds_limits):
        if self.roi_is_valid(Roi(ds_limits)):
            self.ds_roi = Roi(ds_limits)
            self.us_roi.set_x_limit(ds_limits[:2])
        else:
            pub.sendMessage("ROI ERROR")
        pub.sendMessage("ROI CHANGED")

    def set_us_roi(self, us_limits):
        if self.roi_is_valid(Roi(us_limits)):
            self.us_roi = Roi(us_limits)
            self.ds_roi.set_x_limit(us_limits[:2])
        else:
            pub.sendMessage("ROI ERROR")
        pub.sendMessage("ROI CHANGED")

    def set_max_x_limits(self, x_max):
        self.ds_roi.set_x_max(x_max)
        self.us_roi.set_x_max(x_max)

    def set_max_y_limits(self, y_max):
        self.ds_roi.set_y_max(y_max)
        self.us_roi.set_y_max(y_max)

    def set_max_limits(self, x_max, y_max):
        self.set_max_x_limits(x_max)
        self.set_max_y_limits(y_max)

    def set_x_limits(self, x_limits):
        if x_limits[0] < x_limits[1]:
            self.set_x_min(x_limits[0])
            self.set_x_max(x_limits[1])
        else:
            pub.sendMessage("ROI ERROR")
            pub.sendMessage("ROI CHANGED")

    def get_x_limits(self):
        return [self.ds_roi.x_min, self.ds_roi.x_max]

    def set_x_min(self, x_min):
        self.ds_roi.x_min = x_min
        self.us_roi.x_min = x_min
        pub.sendMessage("ROI CHANGED")

    def set_x_max(self, x_max):
        self.ds_roi.x_max = x_max
        self.us_roi.x_max = x_max
        pub.sendMessage("ROI CHANGED")

    @staticmethod
    def roi_is_valid(roi):
        if roi.x_min > roi.x_max:
            return False
        elif roi.y_min > roi.y_max:
            return False
        return True


def black_body_function(wavelength, temp, scaling):
    wavelength = np.array(wavelength) * 1e-9
    c1 = 3.7418e-16
    c2 = 0.014388
    return scaling * c1 * wavelength ** -5 / (np.exp(c2 / (wavelength * temp)) - 1)


def gauss_curve_function(x, scaling, center, sigma):
    return scaling * np.exp(-(x - float(center)) ** 2 / (2 * sigma ** 2))


class TemperatureSettings():
    def __init__(self, data):
        try:
            us_calibration_filename_str = data.get_us_calibration_data().filename
        except AttributeError:
            us_calibration_filename_str = 'Select File...'

        try:
            ds_calibration_filename_str = data.get_ds_calibration_data().filename
        except AttributeError:
            ds_calibration_filename_str = 'Select File...'

        self.ds_calib_file_name = ds_calibration_filename_str
        self.us_calib_file_name = us_calibration_filename_str

        self.ds_etalon_file_name = data.get_ds_calibration_parameter().get_etalon_filename()

        try:
            self.ds_etalon_spectrum = data.ds_calibration_parameter.get_etalon_spectrum()
        except AttributeError:
            self.ds_etalon_spectrum = []

        self.us_etalon_file_name = data.get_us_calibration_parameter().get_etalon_filename()

        try:
            self.us_etalon_spectrum = data.us_calibration_parameter.get_etalon_spectrum()
        except AttributeError:
            self.us_etalon_spectrum = []

        self.ds_calibration_modus = data.get_ds_calibration_parameter().modus
        self.us_calibration_modus = data.get_us_calibration_parameter().modus

        self.ds_calibration_temperature = data.get_ds_calibration_parameter().temp
        self.us_calibration_temperature = data.get_us_calibration_parameter().temp

        self.ds_roi = data.get_roi_data().get_ds_roi()
        self.us_roi = data.get_roi_data().get_us_roi()

        if not data.ds_calibration_data is None:
            try:
                self.ds_img_data = data.ds_calibration_data.get_img_data()
            except:
                self.ds_calibration_spectrum = data.ds_calibration_data.img_data
            self.ds_x_calibration = data.ds_calibration_data.x_whole

        if not data.us_calibration_data is None:
            try:
                self.us_img_data = data.us_calibration_data.get_img_data()
            except:
                self.us_calibration_spectrum = data.us_calibration_data.img_data
            self.us_x_calibration = data.us_calibration_data.x_whole
        self.img_dimension = data.exp_data.get_img_dimension()

    @staticmethod
    def load_settings(settings, data):
        data.roi_data_manager._add(settings.img_dimension, RoiData(settings.ds_roi, settings.us_roi))
        data.roi_data = data.roi_data_manager.get_roi_data(data.exp_data.get_img_dimension())
        data.exp_data.roi_data = data.roi_data

        if not settings.ds_calib_file_name == 'Select File...':
            data.ds_calibration_data = ExpDataFromImgData(settings.ds_img_data, settings.ds_calib_file_name,
                                                          settings.ds_x_calibration, data.roi_data_manager)
        else:
            data.ds_calibration_data = None

        if not settings.us_calib_file_name == 'Select File...':
            data.us_calibration_data = ExpDataFromImgData(settings.us_img_data, settings.us_calib_file_name,
                                                          settings.us_x_calibration, data.roi_data_manager)
        else:
            data.us_calibration_data = None

        data.ds_calibration_parameter.set_etalon_filename(settings.ds_etalon_file_name)
        data.us_calibration_parameter.set_etalon_filename(settings.us_etalon_file_name)
        data.ds_calibration_parameter.set_etalon_function_from_spectrum(settings.ds_etalon_spectrum)
        data.us_calibration_parameter.set_etalon_function_from_spectrum(settings.us_etalon_spectrum)

        data.get_ds_calibration_parameter().set_modus(settings.ds_calibration_modus, False)
        data.get_us_calibration_parameter().set_modus(settings.us_calibration_modus, False)
        data.get_ds_calibration_parameter().set_temperature(settings.ds_calibration_temperature, False)
        data.get_us_calibration_parameter().set_temperature(settings.us_calibration_temperature, False)
        data.calculate_spectra()
        pub.sendMessage("EXP DATA CHANGED")


TraxTemperatureSettings = TemperatureSettings