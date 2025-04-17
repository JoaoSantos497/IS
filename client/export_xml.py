def exportar_xml():
    # Lógica para pegar as tarefas e exportar para XML
    tarefas = []  # Substitua por suas tarefas reais
    xml_data = "<tarefas>"  # Início do XML
    for tarefa in tarefas:
        xml_data += f"<tarefa><titulo>{tarefa['titulo']}</titulo></tarefa>"
    xml_data += "</tarefas>"
    return xml_data