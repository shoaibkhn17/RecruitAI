from faster_whisper import WhisperModel

model = WhisperModel(
    "base",
    device="cpu"
)

def transcribe_audio(audio_path):

    segments, info = model.transcribe(
        audio_path
    )

    text = ""

    for segment in segments:

        text += segment.text + " "

    return text.strip()


def evaluate_answer(text):

    words = len(text.split())

    if words >= 80:

        score = 90

    elif words >= 50:

        score = 75

    elif words >= 20:

        score = 60

    else:

        score = 40

    return {

        "communication_score": score,

        "technical_score": score,

        "overall_score": score

    }