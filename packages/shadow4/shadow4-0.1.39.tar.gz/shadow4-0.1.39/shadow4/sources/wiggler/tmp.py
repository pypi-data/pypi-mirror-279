from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam
electron_beam = S4ElectronBeam(energy_in_GeV=1.9,energy_spread=0,current=0.4)
electron_beam.set_sigmas_all(sigma_x=3.9e-05,sigma_y=3.1e-05,sigma_xp=3.92e-05,sigma_yp=3.92e-05)

#magnetic structure
from shadow4.sources.bending_magnet.s4_bending_magnet import S4BendingMagnet
source = S4BendingMagnet(
                 radius=-5.000014049864217, # from syned BM, can be obtained as S4BendingMagnet.calculate_magnetic_radius(-1.26754, electron_beam.energy())
                 magnetic_field=-1.26754, # from syned BM
                 length=0.345000969440631, # from syned BM = abs(BM divergence * magnetic_radius)
                 emin=1000.0,     # Photon energy scan from energy (in eV)
                 emax=1000.1,     # Photon energy scan to energy (in eV)
                 ng_e=100,     # Photon energy scan number of points
                 flag_emittance=1, # when sampling rays: Use emittance (0=No, 1=Yes)
                 )



#light source
from shadow4.sources.bending_magnet.s4_bending_magnet_light_source import S4BendingMagnetLightSource
light_source = S4BendingMagnetLightSource(name='BendingMagnet', electron_beam=electron_beam, magnetic_structure=source, nrays=5000, seed=5676561)
beam = light_source.get_beam()

beamline.set_light_source(light_source)

# optical element number XX
from syned.beamline.shape import Rectangle
boundary_shape = Rectangle(x_left=-0.001, x_right=0.001, y_bottom=-0.001, y_top=0.001)

from shadow4.beamline.optical_elements.absorbers.s4_screen import S4Screen
optical_element = S4Screen(name='Generic Beam Screen/Slit/Stopper/Attenuator', boundary_shape=boundary_shape,
    i_abs=0, # 0=No, 1=prerefl file_abs, 2=xraylib, 3=dabax
    i_stop=0, thick=0, file_abs='<specify file name>', material='Au', density=19.3)

from syned.beamline.element_coordinates import ElementCoordinates
coordinates = ElementCoordinates(p=27.2, q=0, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
from shadow4.beamline.optical_elements.absorbers.s4_screen import S4ScreenElement
beamline_element = S4ScreenElement(optical_element=optical_element, coordinates=coordinates, input_beam=beam)

beam, footprint = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)


# test plot
if True:
   from srxraylib.plot.gol import plot_scatter
   plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)', plot_histograms=0)
   plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')