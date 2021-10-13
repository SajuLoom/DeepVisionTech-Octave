from flask import *
import sys
import os
import io

app = Flask(__name__, template_folder="template/", static_folder="static/")


@app.route('/', methods=['GET', 'POST'])
def helloworld():

    lig = "This is a demo utterance. This will work when you do not add any utterance."
    filepaths = ["D:/voice/skv.wav",
                 "D:/voice/sathwik.wav", "D:/voice/srini.wav"]
    if request.method == 'POST':
        lig = request.form["textarea"]
        voice = int(request.form.get("voices"))
        # print(voice)
        # print(lig)
    #     return render_template("index.html", output="Hii")
    # else:
    #     return render_template("index.html")

        from encoder.params_model import model_embedding_size as speaker_embedding_size
        from utils.argutils import print_args
        from synthesizer.inference import Synthesizer
        from encoder import inference as encoder
        from vocoder import inference as vocoder
        from pathlib import Path
        from IPython.utils import io
        from IPython.display import Audio
        import soundfile as sf
        import numpy as np
        import librosa
        import argparse
        import torch
        try:
            parser = argparse.ArgumentParser(
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser.add_argument("-e", "--enc_model_fpath", type=Path,
                                default="encoder/saved_models/pretrained.pt")
            parser.add_argument("-s", "--syn_model_dir", type=Path,
                                default="synthesizer/saved_models/pretrained/pretrained.pt")
            parser.add_argument("-v", "--voc_model_fpath", type=Path,
                                default="vocoder/saved_models/pretrained/pretrained.pt")
            # parser.add_argument("--low_mem", action="store_true")
            #parser.add_argument("--no_sound", action="store_true")
            args = parser.parse_args()
            print_args(args, parser)
            # if not args.no_sound:
            #    import sounddevice as sd
            encoder.load_model(args.enc_model_fpath)
            synthesizer = Synthesizer(args.syn_model_dir)
            vocoder.load_model(args.voc_model_fpath)
            # encoder_weights = Path("encoder/saved_models/pretrained.pt")
            # vocoder_weights = Path(
            #     "vocoder/saved_models/pretrained/pretrained.pt")
            # syn_dir = Path(
            #     "synthesizer/saved_models/logs-pretrained/taco_pretrained")
            # encoder.load_model(encoder_weights)
            # synthesizer = Synthesizer(syn_dir)
            # vocoder.load_model(vocoder_weights)
            num_generated = 0
            in_fpath = filepaths[voice]
            print(str(in_fpath))
            preprocessed_wav = encoder.preprocess_wav(in_fpath)
            original_wav, sampling_rate = librosa.load(in_fpath)
            preprocessed_wav = encoder.preprocess_wav(
                original_wav, sampling_rate)
            embed = encoder.embed_utterance(preprocessed_wav)
            print("Created the embedding")
            text = str(lig)
            texts = [text]
            embeds = [embed]
            print(texts)
            print(embeds)
            with io.capture_output() as captured:
                specs = synthesizer.synthesize_spectrograms([text], [embed])
            # specs = synthesizer.synthesize_spectrograms(texts, embeds)
            print("doneee")
            spec = specs[0]
            print("Created the mel spectrogram")
            print("Synthesizing the waveform:")
            generated_wav = vocoder.infer_waveform(spec)
            generated_wav = np.pad(
                generated_wav, (0, synthesizer.sample_rate), mode="constant")
            # if not args.no_sound:
            #    sd.stop()
            #    sd.play(generated_wav, synthesizer.sample_rate)
            fpath = "static/output.wav"
            print(generated_wav.dtype)
            # librosa.output.write_wav(fpath, generated_wav.astype(
            #     np.float32), synthesizer.sample_rate)
            sf.write(fpath, generated_wav.astype(
                np.float32), synthesizer.sample_rate)
            print("\nSaved output as %s\n\n" % fpath)
            return render_template("index.html", output=fpath)
        except Exception as e:
            return render_template("index.html", output="Caught exception: %s" % repr(e))
    else:
        return render_template("index.html")


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
