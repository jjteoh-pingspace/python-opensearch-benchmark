import random
import time
import string
from datetime import datetime

# Dummy data generator


def generate_dummy_data():
    return {
        "skycar": random.randint(1, 999),
        "message": '[' + str(time.time()) + ']' + 'MSEQ_V3: '.join(random.choices(string.ascii_letters + string.digits, k=20)),
        "created": datetime.utcnow().isoformat()
    }
