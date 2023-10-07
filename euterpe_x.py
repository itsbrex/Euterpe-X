# -*- coding: utf-8 -*-
"""Euterpe_X.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/asigalov61/Euterpe-X/blob/main/Euterpe_X.ipynb

# Euterpe X (ver. 4.0)

***

Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect. https://www.nscai.gov/

***

#### Project Los Angeles

#### Tegridy Code 2023

***

# (GPU CHECK)
"""

#@title NVIDIA GPU check
!nvidia-smi

"""# (SETUP ENVIRONMENT)"""

#@title Install dependencies
!git clone --depth 1 https://github.com/asigalov61/Euterpe-X
!pip install huggingface_hub
!pip install torch
!pip install einops
!pip install torch-summary
!pip install sklearn
!pip install tqdm
!pip install matplotlib
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

# Commented out IPython magic to ensure Python compatibility.
#@title Import modules

print('=' * 70)
print('Loading core Euterpe X modules...')

import os
import pickle
import random
import secrets
import statistics
from time import time
import tqdm

from huggingface_hub import hf_hub_download

from google.colab import files

print('=' * 70)
print('Loading main Euterpe X modules...')
import torch

# %cd /content/Euterpe-X

import TMIDIX
from x_transformer import *

# %cd /content/
print('=' * 70)
print('Loading aux Euterpe X modules...')

import matplotlib.pyplot as plt

from torchsummary import summary
from sklearn import metrics

from midi2audio import FluidSynth
from IPython.display import Audio, display

print('=' * 70)
print('Done!')
print('Enjoy! :)')
print('=' * 70)

"""# (LOAD MODEL)

## NOTE: Choose one and do not forget to restart colab runtime if you are switching between the checkpoints
"""

#@title Load Euterpe X Small Model

#@markdown Fast model, 32 layers, 141k MIDIs training corpus

full_path_to_model_checkpoint = "/content/Euterpe-X/Models/Small/Euterpe_X_Small_Trained_Model_58000_steps_0.6865_loss_0.7964_acc.pth" #@param {type:"string"}

#@markdown Model precision option

model_precision = "float16" # @param ["float16", "float32"]

#@markdown float16 == Half precision/double speed

#@markdown float32 == Full precision/normal speed

print('=' * 70)
print('Loading Euterpe X Small Pre-Trained Model...')
print('Please wait...')
print('=' * 70)

if os.path.isfile(full_path_to_model_checkpoint):
  print('Model already exists...')

else:
  hf_hub_download(repo_id='asigalov61/Euterpe-X',
                  filename='Euterpe_X_Small_Trained_Model_58000_steps_0.6865_loss_0.7964_acc.pth',
                  local_dir='/content/Euterpe-X/Models/Small/',
                  local_dir_use_symlinks=False)
print('=' * 70)
print('Instantiating model...')

torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
device_type = 'cuda'
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[model_precision]
ctx = torch.amp.autocast(device_type=device_type, dtype=ptdtype)

SEQ_LEN = 2048

# instantiate the model

model = TransformerWrapper(
    num_tokens = 3344,
    max_seq_len = SEQ_LEN,
    attn_layers = Decoder(dim = 1024, depth = 32, heads = 8)
)

model = AutoregressiveWrapper(model)

model = torch.nn.DataParallel(model)

model.cuda()
print('=' * 70)

print('Loading model checkpoint...')

model.load_state_dict(torch.load(full_path_to_model_checkpoint))
print('=' * 70)

model.eval()

print('Done!')
print('=' * 70)

# Model stats
print('Model summary...')
summary(model)

# Plot Token Embeddings
tok_emb = model.module.net.token_emb.emb.weight.detach().cpu().tolist()

cos_sim = metrics.pairwise_distances(
   tok_emb, metric='cosine'
)
plt.figure(figsize=(7, 7))
plt.imshow(cos_sim, cmap="inferno", interpolation="nearest")
im_ratio = cos_sim.shape[0] / cos_sim.shape[1]
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()
plt.savefig("/content/Euterpe-X-Small-Tokens-Embeddings-Plot.png", bbox_inches="tight")

#@title Load Euterpe X Large Model

#@markdown Slow model, 60 layers, 314k MIDIs training corpus

full_path_to_model_checkpoint = "/content/Euterpe-X/Models/Large/Euterpe_X_Large_Trained_Model_100000_steps_0.477_loss_0.8533_acc.pth" #@param {type:"string"}

#@markdown Model precision option

model_precision = "float16" # @param ["float16", "float32"]

#@markdown float16 == Half precision/double speed

#@markdown float32 == Full precision/normal speed

print('=' * 70)
print('Loading Euterpe X Large Pre-Trained Model...')
print('Please wait...')
print('=' * 70)

if os.path.isfile(full_path_to_model_checkpoint):
  print('Model already exists...')

else:
  hf_hub_download(repo_id='asigalov61/Euterpe-X',
                  filename='Euterpe_X_Large_Trained_Model_100000_steps_0.477_loss_0.8533_acc.pth',
                  local_dir='/content/Euterpe-X/Models/Large',
                  local_dir_use_symlinks=False)

print('=' * 70)
print('Instantiating model...')

torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
device_type = 'cuda'
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[model_precision]
ctx = torch.amp.autocast(device_type=device_type, dtype=ptdtype)

SEQ_LEN = 2048

# instantiate the model

model = TransformerWrapper(
    num_tokens = 3344,
    max_seq_len = SEQ_LEN,
    attn_layers = Decoder(dim = 1024, depth = 60, heads = 8)
)

model = AutoregressiveWrapper(model)

model = torch.nn.DataParallel(model)

model.cuda()
print('=' * 70)

print('Loading model checkpoint...')

model.load_state_dict(torch.load(full_path_to_model_checkpoint))
print('=' * 70)

model.eval()

print('Done!')
print('=' * 70)

# Model stats
print('Model summary...')
summary(model)

# Plot Token Embeddings
tok_emb = model.module.net.token_emb.emb.weight.detach().cpu().tolist()

cos_sim = metrics.pairwise_distances(
   tok_emb, metric='cosine'
)
plt.figure(figsize=(7, 7))
plt.imshow(cos_sim, cmap="inferno", interpolation="nearest")
im_ratio = cos_sim.shape[0] / cos_sim.shape[1]
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()
plt.savefig("/content/Euterpe-X-Large-Tokens-Embeddings-Plot.png", bbox_inches="tight")

"""# (GENERATE)"""

#@title Improv Generation

#@markdown Improv settings

#@markdown NOTE: The improv settings below are just the strong suggestions for the model, not the requirements.

#@markdown Some settings combinations may not work well.

drums_present_or_not = True #@param {type:"boolean"}
first_note_instrument = "Flute" #@param ["Piano", "Guitar", "Bass", "Violin", "Cello", "Harp", "Trumpet", "Sax", "Flute", "Choir", "Organ"]

#@markdown Generation settings

number_of_tokens_tp_generate = 420 #@param {type:"slider", min:30, max:2046, step:30}
number_of_batches_to_generate = 4 #@param {type:"slider", min:1, max:16, step:1}
temperature = 0.9 #@param {type:"slider", min:0.1, max:1, step:0.1}
render_MIDI_to_audio = True # @param {type:"boolean"}

print('=' * 70)
print('Euterpe X Improv Model Generator')
print('=' * 70)

velocities_map = [80, 80, 70, 100, 90, 80, 100, 100, 100, 90, 110, 100]

if drums_present_or_not:
  drumsp = 3330 # Yes
else:
  drumsp = 3329 # No

instruments_list = ["Piano", "Guitar", "Bass", "Violin", "Cello", "Harp", "Trumpet", "Sax", "Flute", 'Drums', "Choir", "Organ"]
first_note_instrument_number = instruments_list.index(first_note_instrument)

outy = [3343, drumsp, 3331+first_note_instrument_number]

print('Selected Improv sequence:')
print(outy)
print('=' * 70)

inp = [outy] * number_of_batches_to_generate

inp = torch.LongTensor(inp).cuda()

with ctx:
  out = model.module.generate(inp,
                        number_of_tokens_tp_generate,
                        temperature=temperature,
                        return_prime=True,
                        verbose=True)

out0 = out.tolist()

print('=' * 70)
print('Done!')
print('=' * 70)

#======================================================================

print('Rendering results...')

for i in range(number_of_batches_to_generate):

  print('=' * 70)
  print('Batch #', i)
  print('=' * 70)

  out1 = out0[i]

  print('Sample INTs', out1[:12])
  print('=' * 70)

  if len(out1) != 0:

      song = out1
      song_f = []

      time = 0
      dur = 0
      channel = 0
      pitch = 0
      vel = 90

      for ss in song:

        if ss > 0 and ss < 256:

            time += ss * 8

        if ss >= 256 and ss < 256+(12*128):

            dur = ((ss-256) % 128) * 30

        if ss >= 256+(12*128) and ss < 256+(12*128)+(12*128):
            channel = (ss-(256+(12*128))) // 128
            pitch = (ss-(256+(12*128))) % 128
            vel = velocities_map[channel]

            song_f.append(['note', time, dur, channel, pitch, vel ])

      detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'Euterpe X',
                                                          output_file_name = '/content/Euterpe-X-Music-Composition_'+str(i),
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                          number_of_ticks_per_quarter=500)


      print('=' * 70)
      print('Displaying resulting composition...')
      print('=' * 70)

      fname = '/content/Euterpe-X-Music-Composition_'+str(i)

      x = []
      y =[]
      c = []

      colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

      for s in song_f:
        x.append(s[1] / 1000)
        y.append(s[4])
        c.append(colors[s[3]])

      if render_MIDI_to_audio:
        FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
        display(Audio(str(fname + '.wav'), rate=16000))

      plt.figure(figsize=(14,5))
      ax=plt.axes(title=fname)
      ax.set_facecolor('black')

      plt.scatter(x,y, c=c)
      plt.xlabel("Time")
      plt.ylabel("Pitch")
      plt.show()

"""# (CUSTOM MIDI)"""

#@title Load Seed MIDI
select_seed_MIDI = "Upload your own custom MIDI" # @param ["Upload your own custom MIDI", "Euterpe-X-Piano-Seed-1", "Euterpe-X-Piano-Seed-2", "Euterpe-X-Piano-Seed-3", "Euterpe-X-Piano-Seed-4", "Euterpe-X-Piano-Seed-5", "Euterpe-X-MI-Seed-1", "Euterpe-X-MI-Seed-2", "Euterpe-X-MI-Seed-3", "Euterpe-X-MI-Seed-4", "Euterpe-X-MI-Seed-5"]
render_MIDI_to_audio = True # @param {type:"boolean"}

if select_seed_MIDI != "Upload your own custom MIDI":
  f = '/content/Euterpe-X/Seeds/'+select_seed_MIDI+'.mid'
  score = TMIDIX.midi2ms_score(open(f, 'rb').read())

else:
  uploaded_MIDI = files.upload()
  score = TMIDIX.midi2ms_score(list(uploaded_MIDI.values())[0])
  f = list(uploaded_MIDI.keys())[0]

print('=' * 70)
print('Euterpe X Seed MIDI Loader')
print('=' * 70)
print('Loading seed MIDI...')
print('=' * 70)
print('File:', f)
print('=' * 70)

#=======================================================
# START PROCESSING

# Convering MIDI to ms score with MIDI.py module


# INSTRUMENTS CONVERSION CYCLE
events_matrix = []
melody_chords_f = []
melody_chords_f1 = []

itrack = 1

patches = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

patch_map = [
            [0, 1, 2, 3, 4, 5, 6, 7], # Piano
            [24, 25, 26, 27, 28, 29, 30], # Guitar
            [32, 33, 34, 35, 36, 37, 38, 39], # Bass
            [40, 41], # Violin
            [42, 43], # Cello
            [46], # Harp
            [56, 57, 58, 59, 60], # Trumpet
            [64, 65, 66, 67, 68, 69, 70, 71], # Sax
            [72, 73, 74, 75, 76, 77, 78], # Flute
            [-1], # Drums
            [52, 53], # Choir
            [16, 17, 18, 19, 20] # Organ
            ]

while itrack < len(score):
  for event in score[itrack]:
      if event[0] == 'note' or event[0] == 'patch_change':
          events_matrix.append(event)
  itrack += 1

events_matrix.sort(key=lambda x: x[1])

events_matrix1 = []

for event in events_matrix:
  if event[0] == 'patch_change':
      patches[event[2]] = event[3]

  if event[0] == 'note':
      event.extend([patches[event[3]]])
      once = False

      for p in patch_map:
          if event[6] in p and event[3] != 9: # Except the drums
              event[3] = patch_map.index(p)
              once = True

      if not once and event[3] != 9: # Except the drums
          event[3] = 15 # All other instruments/patches channel
          event[5] = max(80, event[5])

      if event[3] < 12: # We won't write chans 12-16 for now...
          events_matrix1.append(event)

#=======================================================
# PRE-PROCESSING

# checking number of instruments in a composition
instruments_list_without_drums = list(set([y[3] for y in events_matrix1 if y[3] != 9]))

if len(events_matrix1) > 0 and len(instruments_list_without_drums) > 0:

  # recalculating timings
  for e in events_matrix1:
      e[1] = int(e[1] / 8) # Max 1 seconds for start-times
      e[2] = int(e[2] / 30) # Max 2 seconds for durations

  # Sorting by pitch, then by start-time
  events_matrix1.sort(key=lambda x: x[4], reverse=True)
  events_matrix1.sort(key=lambda x: x[1])

  #=======================================================
  # FINAL PRE-PROCESSING

  melody_chords = []

  pe = events_matrix1[0]

  for e in events_matrix1:
    if e[1] >= 0 and e[2] > 0:

      # Cliping all values...
      tim = max(0, min(255, e[1]-pe[1]))
      dur = max(1, min(127, e[2]))
      cha = max(0, min(11, e[3]))
      ptc = max(1, min(127, e[4]))
      vel = max(1, min(127, e[5]))

      # Writing final note
      melody_chords.append([tim, dur, cha, ptc, vel])

      pe = e

#=======================================================
# Velocities map
#=======================================================

# Default fixed velocities for each channel/instrument
velocities_map = [80, 80, 70, 100, 90, 80, 100, 100, 100, 90, 110, 100]

# Extracting velocities from the MIDI file
for i in range(12):
  vels = [m[4] for m in melody_chords if m[2] == i]

  avg_vel = 0

  if len(vels) > 0:
    avg_vel = int(sum(vels) / len(vels))

  if avg_vel > 20:
    velocities_map[i] = avg_vel

#=======================================================
# MAIN PROCESSING CYCLE
#=======================================================

for m in melody_chords:

  # WRITING EACH NOTE HERE
  time = m[0]
  cha_dur = (m[2] * 128) + m[1]
  cha_ptc = (m[2] * 128) + m[3]

  melody_chords_f.extend([time, cha_dur+256, cha_ptc+1792])
  melody_chords_f1.append([time, cha_dur+256, cha_ptc+1792])

#=======================================================

song = melody_chords_f

song_f = []

time = 0
dur = 0
channel = 0
pitch = 0
vel = 90

for ss in song:

  if ss > 0 and ss < 256:

      time += ss * 8

  if ss >= 256 and ss < 256+(12*128):

      dur = ((ss-256) % 128) * 30

  if ss >= 256+(12*128) and ss < 256+(12*128)+(12*128):
      channel = (ss-(256+(12*128))) // 128
      pitch = (ss-(256+(12*128))) % 128
      vel = velocities_map[channel]

      song_f.append(['note', time, dur, channel, pitch, vel ])

detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                      output_signature = 'Euterpe X',
                                                      output_file_name = '/content/Euterpe-X-Seed-Composition',
                                                      track_name='Project Los Angeles',
                                                      list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                      number_of_ticks_per_quarter=500)

#=======================================================

print('=' * 70)
print('Composition stats:')
print('Composition has', len(melody_chords_f1), 'notes')
print('Composition has', len(melody_chords_f), 'tokens')
print('=' * 70)

print('Displaying resulting composition...')
print('=' * 70)

fname = '/content/Euterpe-X-Seed-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

if render_MIDI_to_audio:
  FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
  display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

#@title Standard/Simple Continuation

#@markdown Generation settings

number_of_prime_tokens = 255 #@param {type:"slider", min:3, max:2046, step:3}
number_of_tokens_to_generate = 210 #@param {type:"slider", min:30, max:2046, step:30}
number_of_batches_to_generate = 4 #@param {type:"slider", min:1, max:16, step:1}
temperature = 0.9 #@param {type:"slider", min:0.1, max:1, step:0.1}

#@markdown Outro generation option

#@markdown NOTE: Outro generation needs at least 200 notes (600 tokens) of sequence length. This option is a strong suggestion to the model, not a requirement, so sometimes model will not generate outro as requested

try_to_generate_outro = False #@param {type:"boolean"}

#@markdown Other settings
include_prime_tokens_in_generated_output = True #@param {type:"boolean"}
allow_model_to_stop_generation_if_needed = False #@param {type:"boolean"}
render_MIDI_to_audio = True # @param {type:"boolean"}

print('=' * 70)
print('Euterpe X Standard Model Generator')
print('=' * 70)

if allow_model_to_stop_generation_if_needed:
  min_stop_token = 3343
else:
  min_stop_token = None

outy = melody_chords_f[:number_of_prime_tokens]

if try_to_generate_outro:
  outy.extend([3328, 3328, 3328])

inp = [outy] * number_of_batches_to_generate

inp = torch.LongTensor(inp).cuda()

with ctx:
  out = model.module.generate(inp,
                        number_of_tokens_to_generate,
                        temperature=temperature,
                        return_prime=include_prime_tokens_in_generated_output,
                        eos_token=min_stop_token,
                        verbose=True)

out0 = out.tolist()
print('=' * 70)
print('Done!')
print('=' * 70)

#======================================================================
print('Rendering results...')

for i in range(number_of_batches_to_generate):

  print('=' * 70)
  print('Batch #', i)
  print('=' * 70)

  out1 = out0[i]

  print('Sample INTs', out1[:12])
  print('=' * 70)

  if len(out) != 0:

      song = out1
      song_f = []

      time = 0
      dur = 0
      channel = 0
      pitch = 0
      vel = 90

      for ss in song:

        if ss > 0 and ss < 256:

            time += ss * 8

        if ss >= 256 and ss < 256+(12*128):

            dur = ((ss-256) % 128) * 30

        if ss >= 256+(12*128) and ss < 256+(12*128)+(12*128):
            channel = (ss-(256+(12*128))) // 128
            pitch = (ss-(256+(12*128))) % 128
            vel = velocities_map[channel]

            song_f.append(['note', time, dur, channel, pitch, vel ])

      detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'Euterpe X',
                                                          output_file_name = '/content/Euterpe-X-Music-Composition_'+str(i),
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                          number_of_ticks_per_quarter=500)
      print('=' * 70)
      print('Displaying resulting composition...')
      print('=' * 70)

      fname = '/content/Euterpe-X-Music-Composition_'+str(i)

      x = []
      y =[]
      c = []

      colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

      for s in song_f:
        x.append(s[1] / 1000)
        y.append(s[4])
        c.append(colors[s[3]])

      if render_MIDI_to_audio:
        FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
        display(Audio(str(fname + '.wav'), rate=16000))

      plt.figure(figsize=(14,5))
      ax=plt.axes(title=fname)
      ax.set_facecolor('black')

      plt.scatter(x,y, c=c)
      plt.xlabel("Time")
      plt.ylabel("Pitch")
      plt.show()

"""# (INPAINT)"""

#@title Pitches/Instruments Inpainting

#@markdown NOTE: You can stop the inpainting at any time to render partial results

#@markdown Inpainting settings

#@markdown Select desired instruments to inpaint (any combination is fine)

Piano = False #@param {type:"boolean"}
Guitar = False #@param {type:"boolean"}
Bass = False #@param {type:"boolean"}
Violin = False #@param {type:"boolean"}
Cello = False #@param {type:"boolean"}
Harp = False #@param {type:"boolean"}
Trumpet = False #@param {type:"boolean"}
Clarinet = False #@param {type:"boolean"}
Flute = False #@param {type:"boolean"}
Drums = False #@param {type:"boolean"}
Choir = False #@param {type:"boolean"}
Organ = False #@param {type:"boolean"}

#@markdown Generation settings

number_of_prime_notes = 64 #@param {type:"slider", min:1, max:512, step:1}
number_of_memory_tokens = 1023 #@param {type:"slider", min:6, max:2046, step:3}
number_of_samples_per_inpainted_note = 4 #@param {type:"slider", min:1, max:16, step:1}
temperature = 0.9 #@param {type:"slider", min:0.1, max:1, step:0.1}
render_MIDI_to_audio = True # @param {type:"boolean"}


inpaint_instrument = []

if Piano:
  inpaint_instrument.append(0)

if Guitar:
  inpaint_instrument.append(1)

if Bass:
  inpaint_instrument.append(2)

if Violin:
  inpaint_instrument.append(3)

if Cello:
  inpaint_instrument.append(4)

if Harp:
  inpaint_instrument.append(5)

if Trumpet:
  inpaint_instrument.append(6)

if Clarinet:
  inpaint_instrument.append(7)

if Flute:
  inpaint_instrument.append(8)

if Drums:
  inpaint_instrument.append(9)

if Choir:
  inpaint_instrument.append(10)

if Organ:
  inpaint_instrument.append(11)


print('=' * 70)
print('Euterpe X Standard Model Generator')
print('=' * 70)

out2 = []

for m in melody_chords_f1[:number_of_prime_notes]:
  out2.extend(m)

for i in tqdm.tqdm(range(number_of_prime_notes, len(melody_chords_f1))):

  try:

    if (melody_chords_f1[i][2]-(256+(12*128))) // 128 in inpaint_instrument:

      out2.extend(melody_chords_f1[i][:2])

      samples = []

      for j in range(number_of_samples_per_inpainted_note):

        inp = torch.LongTensor(out2[-number_of_memory_tokens:]).cuda()

        with ctx:
          out1 = model.module.generate(inp,
                                1,
                                temperature=temperature,
                                return_prime=True,
                                verbose=False)

          with torch.no_grad():
            test_loss, test_acc = model(out1)

        samples.append([out1.tolist()[0][-1], test_acc.tolist()])

      accs = [y[1] for y in samples]
      max_acc = max(accs)
      max_acc_sample = samples[accs.index(max_acc)][0]

      out2.extend([max_acc_sample])
    else:
      out2.extend(melody_chords_f1[i])

  except KeyboardInterrupt:
    print('Stopping inpainting...')
    break

  except Exception as e:
    print('Error', e)
    break

print('=' * 70)
print('Done!')
print('=' * 70)

#==================================================

print('Rendering results...')
print('=' * 70)

if len(out2) != 0:

    song = out2
    song_f = []

    time = 0
    dur = 0
    channel = 0
    pitch = 0
    vel = 90

    for ss in song:

      if ss > 0 and ss < 256:

          time += ss * 8

      if ss >= 256 and ss < 256+(12*128):

            dur = ((ss-256) % 128) * 30

      if ss >= 256+(12*128) and ss < 256+(12*128)+(12*128):
          channel = (ss-(256+(12*128))) // 128
          pitch = (ss-(256+(12*128))) % 128
          vel = velocities_map[channel]

          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Euterpe X',
                                                        output_file_name = '/content/Euterpe-X-Music-Composition',
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)


    print('=' * 70)
    print('Displaying resulting composition...')
    print('=' * 70)

    fname = '/content/Euterpe-X-Music-Composition'

    x = []
    y =[]
    c = []

    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

    for s in song_f:
      x.append(s[1] / 1000)
      y.append(s[4])
      c.append(colors[s[3]])

    FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
    display(Audio(str(fname + '.wav'), rate=16000))

    plt.figure(figsize=(14,5))
    ax=plt.axes(title=fname)
    ax.set_facecolor('black')

    plt.scatter(x,y, c=c)
    plt.xlabel("Time")
    plt.ylabel("Pitch")
    plt.show()

"""# (HARMONIZE)"""

#@title Melody Harmonization

#@markdown NOTE: You can stop the generation at any time to render partial results

melody_instrument = "Violin" #@param ["Piano", "Guitar", "Bass", "Violin", "Cello", "Harp", "Trumpet", "Sax", "Flute", "Choir", "Organ"]
number_of_prime_melody_notes = 4 # @param {type:"slider", min:0, max:50, step:1}
number_of_memory_tokens = 2046 # @param {type:"slider", min:33, max:2046, step:3}
temperature = 0.9 #@param {type:"slider", min:0.1, max:1, step:0.1}
render_MIDI_to_audio = True # @param {type:"boolean"}

print('=' * 70)
print('Euterpe X Simple Melody Harmonization Model Generator')

print('=' * 70)
print('Extracting melody...')
#=======================================================

instruments_list = ["Piano", "Guitar", "Bass", "Violin", "Cello", "Harp", "Trumpet", "Sax", "Flute", 'Drums', "Choir", "Organ"]
melody_instrument_number = instruments_list.index(melody_instrument)

melody = []
pe = events_matrix1[0]

for e in events_matrix1:
    if e[3] != 9:

      # Cliping all values...
      time = max(0, min(255, e[1]-pe[1]))
      dur = max(1, min(127, e[2]))
      cha = melody_instrument_number
      ptc = max(1, min(127, e[4]))

      if ptc < 60:
        ptc_aug = (ptc % 12) + 60
      else:
        ptc_aug = ptc

      # WRITING EACH NOTE HERE
      cha_dur = (cha * 128) + dur
      cha_ptc = (cha * 128) + ptc_aug

      if time != 0:
        melody.append([time, cha_dur+256, cha_ptc+1792])

      pe = e

melody[0][0] = 0

#=======================================================

print('=' * 70)
print('Melody has', len(melody), 'notes')
print('Melody has', len(melody)*3, 'tokens')

print('=' * 70)
print('Starting harmonization...')
print('=' * 70)

outy = []

for m in melody[:number_of_prime_melody_notes]:
  outy.extend(m)

next_chord_time = 0
chord_time_delta = 0
cur_time = 0

for i in tqdm.tqdm(range(number_of_prime_melody_notes, len(melody))):

  try:
    outy.extend(melody[i])

    #====================================================

    outy.extend([0])

    inp = [outy[-number_of_memory_tokens:]]
    inp = torch.LongTensor(inp).cuda()

    with ctx:
      out = model.module.generate(inp,
                            2,
                            temperature=temperature,
                            return_prime=False,
                            eos_token=None,
                            verbose=False)

    out0 = out.tolist()[0]



    if (((out0[1]-(256+(12*128))) // 128) != melody_instrument_number):
      outy.extend(out0)
    else:
      outy.pop()

    #====================================================

    out0 = [0, 0, 0]
    pout0 = []

    while out0[0] == 0 and out0 != pout0:

      pout0 = out0

      inp = [outy[-number_of_memory_tokens:]]
      inp = torch.LongTensor(inp).cuda()

      with ctx:
        out = model.module.generate(inp,
                              3,
                              temperature=temperature,
                              return_prime=False,
                              eos_token=None,
                              verbose=False)

      out0 = out.tolist()[0]

      if out0[0] == 0 and (((out0[2]-(256+(12*128))) // 128) != melody_instrument_number) and out0 != pout0:
        outy.extend(out0)

    #====================================================

  except KeyboardInterrupt:
    break

  except Exception as e:
    print('Error', e)
    break

print('=' * 70)
print('Done!')
print('=' * 70)

#======================================================================

print('Rendering results...')
print('=' * 70)

out1 = outy

print('Sample INTs', out1[:12])
print('=' * 70)

if len(out1) != 0:

    song = out1
    song_f = []

    time = 0
    dur = 0
    channel = 0
    pitch = 0
    vel = 90

    for ss in song:

      if ss > 0 and ss < 256:

          time += ss * 8

      if ss >= 256 and ss < 256+(12*128):

          dur = ((ss-256) % 128) * 30

      if ss >= 256+(12*128) and ss < 256+(12*128)+(12*128):
          channel = (ss-(256+(12*128))) // 128
          pitch = (ss-(256+(12*128))) % 128
          vel = velocities_map[channel]

          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Euterpe X',
                                                        output_file_name = '/content/Euterpe-X-Music-Composition',
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)


    print('=' * 70)
    print('Displaying resulting composition...')
    print('=' * 70)

    fname = '/content/Euterpe-X-Music-Composition'

    x = []
    y =[]
    c = []

    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

    for s in song_f:
      x.append(s[1] / 1000)
      y.append(s[4])
      c.append(colors[s[3]])

    if render_MIDI_to_audio:
      FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
      display(Audio(str(fname + '.wav'), rate=16000))

    plt.figure(figsize=(14,5))
    ax=plt.axes(title=fname)
    ax.set_facecolor('black')

    plt.scatter(x,y, c=c)
    plt.xlabel("Time")
    plt.ylabel("Pitch")
    plt.show()

"""# Congrats! You did it! :)"""