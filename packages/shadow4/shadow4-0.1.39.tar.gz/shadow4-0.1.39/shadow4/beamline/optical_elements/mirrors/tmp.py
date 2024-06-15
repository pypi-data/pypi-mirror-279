from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam

electron_beam = S4ElectronBeam(energy_in_GeV=6, energy_spread=0.001, current=0.2)
electron_beam.set_sigmas_all(sigma_x=3.01836e-05, sigma_y=4.36821e-06, sigma_xp=3.63641e-06, sigma_yp=1.37498e-06)

# magnetic structure
from shadow4.sources.undulator.s4_undulator_gaussian import S4UndulatorGaussian

source = S4UndulatorGaussian(
    period_length=0.017,  # syned Undulator parameter (length in m)
    number_of_periods=117.6470588235294,  # syned Undulator parameter
    photon_energy=15000.0,  # Photon energy (in eV)
    delta_e=0.0,  # Photon energy width (in eV)
    ng_e=100,  # Photon energy scan number of points
    flag_emittance=1,  # when sampling rays: Use emittance (0=No, 1=Yes)
    flag_energy_spread=0,  # when sampling rays: Use e- energy spread (0=No, 1=Yes)
    harmonic_number=1,  # harmonic number
    flag_autoset_flux_central_cone=0,  # value to set the flux peak
    flux_central_cone=10000000000.0,  # value to set the flux peak
)

# light source
from shadow4.sources.undulator.s4_undulator_gaussian_light_source import S4UndulatorGaussianLightSource

light_source = S4UndulatorGaussianLightSource(name='GaussianUndulator', electron_beam=electron_beam,
                                              magnetic_structure=source, nrays=50000, seed=5676561)
beam = light_source.get_beam()

beamline.set_light_source(light_source)

# optical element number XX
from syned.beamline.shape import Rectangle

boundary_shape = Rectangle(x_left=-0.00025, x_right=0.00025, y_bottom=-0.00025, y_top=0.00025)

from shadow4.beamline.optical_elements.absorbers.s4_screen import S4Screen

optical_element = S4Screen(name='PS', boundary_shape=boundary_shape,
                           i_abs=0,  # 0=No, 1=prerefl file_abs, 2=xraylib, 3=dabax
                           i_stop=0, thick=0, file_abs='<specify file name>', material='Au', density=19.3)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=27.066, q=0, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
from shadow4.beamline.optical_elements.absorbers.s4_screen import S4ScreenElement

beamline_element = S4ScreenElement(optical_element=optical_element, coordinates=coordinates, input_beam=beam)

beam, footprint = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# optical element number XX
from syned.beamline.shape import Rectangle

boundary_shape = Rectangle(x_left=-0.04, x_right=0.04, y_bottom=-0.3, y_top=0.3)

from shadow4.beamline.optical_elements.mirrors.s4_toroid_mirror import S4ToroidMirror

optical_element = S4ToroidMirror(name='Toroid Mirror', boundary_shape=boundary_shape,
                                 surface_calculation=1,
                                 min_radius=0.046,  # min_radius = sagittal
                                 maj_radius=7500,  # maj_radius = tangential
                                 f_torus=0,
                                 p_focus=44.54, q_focus=11.75, grazing_angle=0.00249,
                                 f_reflec=0, f_refl=0, file_refl='<none>', refraction_index=0.99999 + 0.001j,
                                 coating_material='Si', coating_density=2.33, coating_roughness=0)
ideal_mirror = optical_element
boundary_shape = None

from shadow4.beamline.optical_elements.mirrors.s4_numerical_mesh_mirror import S4NumericalMeshMirror

optical_element = S4NumericalMeshMirror(name='Numerical Mesh Mirror', boundary_shape=boundary_shape,
                                        xx=None, yy=None, zz=None, surface_data_file='/users/srio/Oasys/toroidal_mirror.hdf5',
                                        f_reflec=0, f_refl=0, file_refl='', refraction_index=1,
                                        coating_material='', coating_density=1, coating_roughness=0)
numerical_mesh_mirror = optical_element
from syned.beamline.shape import Rectangle

boundary_shape = Rectangle(x_left=-0.04, x_right=0.04, y_bottom=-0.3, y_top=0.3)

from shadow4.beamline.optical_elements.mirrors.s4_additional_numerical_mesh_mirror import \
    S4AdditionalNumericalMeshMirror

optical_element = S4AdditionalNumericalMeshMirror(name='ideal + error Mirror', ideal_mirror=ideal_mirror,
                                                  numerical_mesh_mirror=numerical_mesh_mirror)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=17.474, q=0, angle_radial=1.568306327, angle_azimuthal=0,
                                 angle_radial_out=1.568306327)
movements = None
from shadow4.beamline.optical_elements.mirrors.s4_additional_numerical_mesh_mirror import \
    S4AdditionalNumericalMeshMirrorElement

beamline_element = S4AdditionalNumericalMeshMirrorElement(optical_element=optical_element, coordinates=coordinates,
                                                          movements=movements, input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# test plot
if True:
    from srxraylib.plot.gol import plot_scatter

    # plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)',
    #              plot_histograms=0)
    plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns',show=0)
    plot_scatter(1e6 * beam.get_column(4, nolost=1), 1e6 * beam.get_column(6, nolost=1), title='(Xp,Zp) in microns')