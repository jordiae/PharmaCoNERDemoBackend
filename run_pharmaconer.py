import os
import random
import string
import time
PHARMACONER_PATH = '/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/src/CustomNeuroNER/'
DATA_PATH = os.path.join(PHARMACONER_PATH, 'data')
# OUTPUT_PATH = os.path.join(PHARMACONER_PATH, 'output')
OUTPUT_PATH = '/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/task/deploy_test_output2'
# PARAMETERS_PATH = 'pharmaconer_deploy_parameters.ini'
PARAMETERS_PATH = os.path.join('/home/jordiae/PycharmProjects/PharmaCoNERDemoBackend', 'pharmaconer_deploy_parameters.ini')

sample_text = '''Presentamos el caso de una mujer de 70 años, con antecedentes de hipertensión arterial, hernia de hiato, estreñimiento e histerectomía que consultó por síndrome miccional irritativo desde hacía 8 meses, consistente en disuria y polaquiuria intensas con urgencias miccionales ocasionales sin otra sintomatología urológica añadida. En los últimos 6 meses había presentado 3 episodios de infección del tracto urinario bajo con urocultivos positivos a E. coli tratados por su médico de cabecera.
El estudio inicial incluyó bioquímica sanguínea que fue normal, orina y estudio de sedimento de orina que mostraron intensa leucocituria, urocultivo que fue de nuevo positivo a E.coli y una citología urinaria por micción espontánea cuyo resultado fue células uroteliales sin atipias y abundantes leucocitos polimorfonucleares neutrófilos. Se prescribió tratamiento con antibioteparia y anticolinérgico (tolterodina).
A los 3 meses la paciente fue revisada en consulta externa, persistiendo la sintomatología basada en disuria y polaquiuria, si bien había mejorado bastante de las urgencias con el anticolinérgico, e incluso días antes dela revisión había tenido nuevo episodio de infección urinaria.
Ante la escasa respuesta encontrada, se inició un estudio más avanzado, solicitando urografía intravenosa para descartar tumor urotelial del tracto urinario superior, la cual fue rigurosamente normal, y ecografía urológica que también fue normal, por lo que se realizó cistoscopia en consulta, hallando lesiones nodulares, sobreelevadas, de aspecto sólido, discretamente enrojecidas, con áreas adyacentes de edema, localizadas en trígono y parte inferior de ambas caras laterales. Debido a este hallazgo, a pesar de que la paciente no tenía factores de riesgo para TBC y la urografía fue rigurosamente normal, se realizó baciloscopia en orina y cultivo Lowenstein-Jensen de 6 muestras de la primera orina de la mañana en días consecutivos, ya que las lesiones vesicales macroscópicamente podrían tratarse de tuberculomas, siendo estos estudios negativos para bacilo de Koch, por lo que se realizó resección endoscópica de las lesiones descritas bajo anestesia. El estudio anatomopatológico reveló ulceración de la mucosa con importante infiltrado inflamatorio crónico y congestión vascular, así como la presencia de células plasmáticas y linfocitos constituyendo folículos linfoides, los cuales están divididos en una zona central donde abundan linfoblastos e inmunoblastos, llamado centro germinativo claro, y una zona periférica formada por células maduras (linfocitos y células plasmáticas) dando lugar a los linfocitos del manto o corona radiada, como también se les denomina.

A la paciente se le indicó medidas higiénico-dietéticas y profilaxis antibiótica mantenida ciclo largo a dosis única diaria nocturna 3 meses y posteriormente días alternos durante 6 meses con ciprofloxacino, vitamina A dosis única diaria 6 meses, prednisona 30mg durante 45 días y posteriormente en días alternos durante otros 45 días hasta su suspensión definitiva, y por último protección digestiva con omeprazol. La paciente experimentó clara mejoría con desaparición progresiva de la clínica, sobre todo a partir del tercer mes de tratamiento.
Actualmente (al año de finalización del tratamiento), se encuentra asintomática con cistoscopia de control normal y urocultivos negativos.'''


def random_string(length=10):
    """Generate a random string of fixed length (lowercase letters)
    From https://pynative.com/python-generate-random-string/ """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def prepare_data(id, text):
    """Generate deploy set with the input text"""
    # text = sample_text
    os.mkdir(os.path.join(DATA_PATH, id))
    os.mkdir(os.path.join(DATA_PATH, id, 'deploy'))
    with open(os.path.join(DATA_PATH, id, 'deploy', 'data.txt'), 'w') as f:
        f.write(text)


def get_annotations(id):
    """Get annotations from BRAT file output by PharmaCoNER"""
    filenames = os.listdir(OUTPUT_PATH)
    found = False
    for filename in filenames:
        if filename.startswith(id):
            found = True
            break
    if not found:
        return 'Failed to get annotations'
    with open(os.path.join(OUTPUT_PATH, filename, 'brat', 'deploy', 'data.ann'), 'r') as f:
        ann = f.read()
    '''
    os.system('rm ' + os.path.join(OUTPUT_PATH, filename, 'brat', 'data.ann'))
    os.system('rm ' + os.path.join(OUTPUT_PATH, filename, 'brat', 'data.txt'))
    os.system('rmdir' + os.path.join(OUTPUT_PATH, filename))
    os.system('rm -rf ' + os.path.join(DATA_PATH, id, 'deploy'))
    '''

    return ann


def run_pharmaconer(text):
    """Call PharmaCoNER"""
    time0 = time.time()
    id = random_string()
    prepare_data(id, text)
    print('Running PharmaCoNER')
    print('/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/src/CustomNeuroNER/bin/python  ' + os.path.join(
        '/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/src/CustomNeuroNER/', 'src',
        'main.py') + ' --parameters_filepath ' + PARAMETERS_PATH + ' --dataset_text_folder ' + os.path.join(DATA_PATH, id) + ' --experiment_name ' + id)
    os. chdir(os.path.join(
        '/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/src/CustomNeuroNER/', 'src'))
    os.system('/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/src/CustomNeuroNER/bin/python  ' + os.path.join(
        '/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/src/CustomNeuroNER/', 'src',
        'main.py') + ' --parameters_filepath ' + PARAMETERS_PATH + ' --dataset_text_folder ' + os.path.join(DATA_PATH, id) + ' --experiment_name ' + id)
    ann = get_annotations(id)
    time1 = time.time()
    res = 'Tagged text in ' + str(time1-time0) + ' seconds:\n\n' + text + '\n\n' + ann
    return res
