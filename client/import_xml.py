import xml.etree.ElementTree as ET

def importar_xml(xml_data):
    root = ET.fromstring(xml_data)
    tarefas = []
    for tarefa_element in root.findall('tarefa'):
        titulo = tarefa_element.find('titulo').text
        tarefas.append({"titulo": titulo})
    print(f"Tarefas importadas: {tarefas}")
