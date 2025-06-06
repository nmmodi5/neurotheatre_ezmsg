import argparse

import ezmsg.core as ez

from ezmsg.unicorn.device import UnicornSettings
from ezmsg.panel.application import Application, ApplicationSettings
from ezmsg.sigproc.butterworthfilter import ButterworthFilterSettings
from ezmsg.panel.timeseriesplot import TimeSeriesPlotSettings
from neurotheatre.osc import OSCSystem, OSCSystemSettings, EEGOSCSettings

from neurotheatre.injector import InjectorSettings
from neurotheatre.midiunit import MidiSettings
from neurotheatre.bandunit import BandUnitSettings
from neurotheatre.signal_to_midi import SignalToMidiSystem, SignalToMidiSystemSettings
from neurotheatre.signal_to_band import WaveSystem, WaveSystemSettings

def osc():

    parser = argparse.ArgumentParser(description = 'unicorn OSC client')
    parser.add_argument('-d', '--device', help = 'device address', default = 'simulator')
    parser.add_argument('--td-address', help = 'remote OSC server address, default: 127.0.0.1:8000', default = '127.0.0.1:8000')
    parser.add_argument('--imu-address', help = 'remote imu server address, default: 127.0.0.1:9001', default = '127.0.0.1:9001')
    parser.add_argument('--hand-address', help = 'remote hand server address, default: 127.0.0.1:8002', default = '127.0.0.1:8002')
    parser.add_argument('--blocksize', help = 'eeg sample block size @ 200 Hz', default = 10, type = int)
    parser.add_argument('--jaw_thresh', help = 'Jaw Clenching decoding threshold frequency', default = '20.0', type = float)

    class Args:
        device: str
        td_address: str
        imu_address: str
        hand_address: str
        blocksize: int
        jaw_thresh: float

    args = parser.parse_args(namespace = Args)

    osc = OSCSystem(
        OSCSystemSettings(
            osc_settings = EEGOSCSettings(
                td_address = args.td_address,
                imu_address = args.imu_address,
                hand_address = args.hand_address,
                jaw_thresh = args.jaw_thresh
            ),
            unicorn_settings = UnicornSettings(
                address = args.device,
                n_samp = args.blocksize
            )
        )
    )

    app = Application(
        ApplicationSettings(
            port = 8888,
            name = 'Neurotheatre'
        )
    )

    app.panels = {
        'osc': osc.DASHBOARD.app,
    }

    ez.run(
        OSC = osc,
        APP = app,
    )

def museosc():

    from neurotheatre.osc import MuseOSCSystem, MuseOSCSystemSettings
    from neurotheatre.muse.musedevice import MuseUnitSettings

    parser = argparse.ArgumentParser(description='Muse OSC client')
    parser.add_argument('-d', '--device', help='Muse device name (leave empty for auto-detection)', default=None)
    parser.add_argument('-a', '--address', help='Remote OSC server address', default='localhost')
    parser.add_argument('-p', '--port', help='Remote OSC server port (UDP)', default=8000, type=int)
    parser.add_argument('--blocksize', help = 'eeg sample block size @ 256 Hz', default = 10, type = int)

    class Args:
        muse_name: str
        address: str
        port: int

    args = parser.parse_args(namespace=Args)

    museosc = MuseOSCSystem(
        MuseOSCSystemSettings(
            muse_settings=MuseUnitSettings(
                muse_name=args.device,
                blocksize=args.blocksize,
            ),
            osc_settings=EEGOSCSettings(
                address=args.address,
                port=args.port,
            ),
            plot_settings=TimeSeriesPlotSettings(
                name="Muse EEG Data",
                downsample_factor=2,
            ),
        )
    )

    app = Application(
        ApplicationSettings(
            port=8888,
            name='MuseOSC'
        )
    )

    app.panels = {
        'muse_osc': museosc.PLOT.app
    }

    ez.run(
        MUSEOSC=museosc,
        APP=app,
    )

def to_audio():

    from neurotheatre.audioloopback import AudioLoopbackSettings

    from neurotheatre.signal_to_audio import SignalToAudioSystem, SignalToAudioSystemSettings
    from neurotheatre.upsample import UpsampleSettings

    parser = argparse.ArgumentParser(description = 'unicorn OSC client')
    parser.add_argument('-d', '--device', help = 'device address', default = 'simulator')
    parser.add_argument('--blocksize', help = 'eeg sample block size @ 200 Hz', default = 10, type = int)


    class Args:
        device: str
        address: str
        port: int
        blocksize: int

    args = parser.parse_args(namespace = Args)

    signaltoaudio = SignalToAudioSystem(
        SignalToAudioSystemSettings(
            unicorn_settings = UnicornSettings(
                address = args.device,
                n_samp = args.blocksize
            ),

            injector_settings = InjectorSettings(
                enabled = False,
                freq = 440,
            ),

            butterworth_filter_settings = ButterworthFilterSettings(
                axis = 'time',
                order = 3, 
                cuton = 1.0, 
                cutoff = 30.0,
            ),

            upsample_settings= UpsampleSettings(
                axis = 'time',
                factor = 3,
            ),

            audio_settings= AudioLoopbackSettings(
                sample_rate= 44100,
                channels= 1,
            ),
        )
    )

    app = Application(
        ApplicationSettings(
            port = 8888,
            name = 'Neurotheatre'
        )
    )

    app.panels = {
        'signal_to_audio': signaltoaudio.DASHBOARD.app,
    }

    ez.run(
        SIGNALTOAUDIO = signaltoaudio,
        APP = app,
    )

def to_midi():
    parser = argparse.ArgumentParser(description='unicorn MIDI client')
    parser.add_argument('-d', '--device', help='device address', default='simulator')
    parser.add_argument('--blocksize', help='eeg sample block size @ 200 Hz', default=10, type=int)
    parser.add_argument('--midiport', help='MIDI Output port name', default='GarageBand Virtual In')

    class Args:
        device: str
        blocksize: int
        midiport: str

    args = parser.parse_args(namespace=Args)

    signaltomidi = SignalToMidiSystem(
        SignalToMidiSystemSettings(
            unicorn_settings=UnicornSettings(
                address=args.device,
                n_samp=args.blocksize
            ),

            injector_settings=InjectorSettings(
                enabled=False,
                freq=440,
            ),

            butterworth_filter_settings=ButterworthFilterSettings(
                axis='time',
                order=3,
                cuton=1.0,
                cutoff=30.0,
            ),

            midi_settings=MidiSettings(
                midi_port=args.midiport,
                channel=0,
                note_range=(21, 108),
                velocity=64,
            ),
        )
    )

    app = Application(
        ApplicationSettings(
            port=8888,
            name='Neurotheatre'
        )
    )

    app.panels = {
        'signal_to_midi': signaltomidi.DASHBOARD.app,
    }

    ez.run(
        SIGNALTOMIDI=signaltomidi,
        APP=app,
    )

def to_band():
    parser = argparse.ArgumentParser(description='Unicorn to dominant frequency wave')
    parser.add_argument('-d', '--device', help='Device address', default='simulator')
    parser.add_argument('--blocksize', help='EEG sample block size @ 256 Hz', default=10, type=int)
    parser.add_argument('--samplingrate', help='sampling rate for FFT', default=256.0, type=float)

    class Args:
        device: str
        blocksize: int
        samplingrate: float

    args = parser.parse_args(namespace=Args)

    wavesystem = WaveSystem(
        WaveSystemSettings(
            wave_settings=BandUnitSettings(
                sampling_rate=args.samplingrate,
            ),
            unicorn_settings=UnicornSettings(
                address=args.device,
                n_samp=args.blocksize,
            ),
        )
    )

    app = Application(
        ApplicationSettings(
            port=8888,
            name='WaveSystem'
        )
    )

    app.panels = {
        'wave_system': wavesystem.DASHBOARD.app,
    }

    ez.run(
        WAVESYSTEM=wavesystem,
        APP=app,
    )

def to_jawclench():
    parser = argparse.ArgumentParser(description='Unicorn to dominant frequency wave')
    parser.add_argument('-d', '--device', help='Device address', default='simulator')
    parser.add_argument('--blocksize', help='EEG sample block size @ 256 Hz', default=10, type=int)
    parser.add_argument('--samplingrate', help='sampling rate for FFT', default=256.0, type=float)

    class Args:
        device: str
        blocksize: int
        samplingrate: float

    args = parser.parse_args(namespace=Args)

    jawclenchsystem = WaveSystem(
        WaveSystemSettings(
            wave_settings=BandUnitSettings(
                sampling_rate=args.samplingrate,
                # Detect gamma band and return True/False
                # THis is the crux of Jaw Clench Detection logic
                detect_band=('gamma', True),
            ),
            unicorn_settings=UnicornSettings(
                address=args.device,
                n_samp=args.blocksize,
            ),
        )
    )

    app = Application(
        ApplicationSettings(
            port=8888,
            name='jawclenchsystem'
        )
    )

    app.panels = {
        'jawclench_system': jawclenchsystem.DASHBOARD.app,
    }

    ez.run(
        JAWCLENCHSYSTEM=jawclenchsystem,
        APP=app,
    )