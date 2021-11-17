import pickle
from datetime import date
import re
import legislacao

def ache(exp_reg, tex):
    """Recebe uma expressão regular e retorna uma tupla com o
    início da ocorrência e seu tamanho. (-1, -1) se não encontrada"""
    re_ache = re.compile(exp_reg)
    oco = re_ache.search(tex)
    if oco:
        return oco.span()[0], oco.span()[1] - oco.span()[0]
    else:
        return -1, -1

def cria_no(k):
    data = '{}-{}-{}'.format(k[2].year, k[2].month, k[2].day)
    n3_t = "<"+tipo_lei[k[0]]+"#"+k[1]+"#"+data+">\n"
    n3_t += "    rdf:type eli:LegalResource ;\n"
    n3_t += '    eli:date_publication "'+'{} - {} - {}'.format(k[2].year, k[2].month, k[2].day)+'"^^xsd:date ;\n'
    n3_t += '    eli:description "' + dic_leg[k].ementa.replace('"', '').replace('\n', ' ') + '" ;\n'
    n3_t += '    eli:type_document "'+tipo_doc[k[0]]+'" ;\n'
    n3_t += '    eli:number "'+k[1]+'"'
    if len(dic_leg[k].altera) > 0:
        for leg in dic_leg[k].altera:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t  += " ;\n    eli:changes "+"<"+tipo_lei[leg[0]]+"#"+leg[1]+"#"+data+">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'altera', leg)
    if len(dic_leg[k].e_alterada_por) > 0:
        for leg in dic_leg[k].e_alterada_por:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t  += " ;\n    eli:changed_by "+"<"+tipo_lei[leg[0]]+"#"+leg[1]+"#"+data+">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'é alterada por', leg)
    if len(dic_leg[k].cita) > 0:
        for leg in dic_leg[k].cita:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t += " ;\n    eli:cites " + "<" + tipo_lei[leg[0]] + "#" + leg[1] + "#" + data + ">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'cita', leg)
    if len(dic_leg[k].e_citada_por) > 0:
        for leg in dic_leg[k].e_citada_por:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t += " ;\n    eli:cited_by " + "<" + tipo_lei[leg[0]] + "#" + leg[1] + "#" + data + ">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'é citada por', leg)
    if len(dic_leg[k].revoga) > 0:
        for leg in dic_leg[k].revoga:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t += " ;\n    eli:repeals " + "<" + tipo_lei[leg[0]] + "#" + leg[1] + "#" + data + ">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'revoga', leg)
    if len(dic_leg[k].e_revogada_por) > 0:
        for leg in dic_leg[k].e_revogada_por:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t += " ;\n    eli:repealed_by " + "<" + tipo_lei[leg[0]] + "#" + leg[1] + "#" + data + ">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'é revogada por', leg)
    if len(dic_leg[k].regulamenta) > 0:
        for leg in dic_leg[k].regulamenta:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t += " ;\n    eli:consolidates " + "<" + tipo_lei[leg[0]] + "#" + leg[1] + "#" + data + ">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'regulamenta', leg)
    if len(dic_leg[k].e_regulamentada_por) > 0:
        for leg in dic_leg[k].e_regulamentada_por:
            data = '{}-{}-{}'.format(leg[2].year, leg[2].month, leg[2].day)
            n3_t += " ;\n    eli:consolidated_by " + "<" + tipo_lei[leg[0]] + "#" + leg[1] + "#" + data + ">"
            if not leg in legis_inseridas:
                try:
                    dic_leg[leg]
                    legis.append(leg)
                    legis_inseridas.append(leg)
                except KeyError:
                    print('***', k, 'é regulamentada por', leg)
    return n3_t


tipo_lei = ('LeiOrd', 'Dec', 'LeiCom', 'DecLei', 'LeiDel', 'MPa32', 'MPp32',
            'Consti', 'DecLeg', 'LeiEst', 'LComEs')
tipo_doc = ('Lei Ordinária Federal', 'Decreto', 'Lei Complementar Federal', 'Decreto-Lei',
            'Lei Delegada', 'Medida Provisória Ant32', 'Medida Provisória Pos32',
            'Constituição', 'Decreto Legislativo', 'Lei Estadual (CE)',
            'Lei Complementar Estadual (CE)')
legis = []
legis_inseridas = []

fp = open('dicionario_legislacao.dic', 'rb')
dic_leg = pickle.load(fp)
fp.close()

n3_t = "@base <http://example.org/> .\n"
n3_t += "@prefix rdf: <http://www.w3.org/1999/02/22−rdf−syntax−ns#> .\n"
n3_t += "@prefix eli: <http://data.europa.eu/eli/ontology#> .\n"
n3_t += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#date> .\n\n"

# c = 0
for k, v in dic_leg.items():
    if not k in legis_inseridas:
        legis.append(k)
        legis_inseridas.append(k)
    while len(legis) > 0:
        k = legis.pop(0)
        # print('*****', k)
        n3_t += cria_no(k)
        n3_t += " .\n\n"
        # c += 1
        # if c > 10:
        #     break

# print(n3_t)

fp = open('rdf_graph_v3.ttl', 'w', encoding="utf-8")
fp.write(n3_t)
fp.close()
