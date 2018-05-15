import networkx as nx
from itertools import islice


def shortest_path_basis_weight(g, source, target):
    return nx.dijkstra_path(g, source, target)


def k_shortest_paths_default(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source,
                                                target, weight=weight), k))


def transform_function(current, aim, g):
    nodes = g.nodes()
    mapping = {
        'software engineer & architect': 'software engineer',
        'vp of marketing & business development': 'vp marketing',
        'bachelor of computer science':
        'bachelor of science in computer science',
        'btech in computer science': 'bachelor of science in computer science',
        'bs in computer science': 'bachelor of science in computer science',
        'masters of computer science': 'master of science in computer science',
        'mtech in computer science': 'master of science in computer science',
        'ms in computer science': 'master of science in computer science',
        'bachelor of data science': 'bachelor of science in data science',
        'btech in data science': 'bachelor of science in data science',
        'bs in data science': 'bachelor of science in data science',
        'masters of data science': 'master of science in data science',
        'mtech in data science': 'master of science in data science',
        'ms in data science': 'master of science in data science',
        'bachelor of electrical engineering':
        'bachelor of science in electrical engineering',
        'btech in electrical engineering':
        'bachelor of science in electrical engineering',
        'bs in electrical engineering':
        'bachelor of science in electrical engineering',
        'masters of electrical engineering':
        'master of science in electrical engineering',
        'mtech in electrical engineering':
        'master of science in electrical engineering',
        'ms in electrical engineering':
        'master of science in electrical engineering',
        'bs in mathematics': 'bachelor of science in mathematics',
        'masters of mathematics': 'master of science in mathematics',
        'mtech in mathematics': 'master of science in mathematics',
        'ms in mathematics': 'master of science in mathematics',
        'bachelor in mathematics': 'bachelor of science in mathematics',
        'bachelors in mathematics': 'bachelor of science in mathematics',
        'data science': 'data science',
        'financial analyst': 'financial analyst',
        'engineering': 'engineer',
        'engineering manager': 'engineer manager',
        'in advertising': 'advertising',
        'sales associate': 'sales',
        'lead technical / business strategist / dmts': 'business analyst',
        'strategy director / dmts': 'business analyst',
        'product architects': 'product architect',
        'PharmD': 'doctor',
        'microprocessor engineer - team lead': 'engineer',
        'B.S. in Electrical & Electronics':
        'Bachelor of Science in Electrical & Electronics',
        'recruiter': 'recruiter',
        'director of facilities & plant operations': 'director of operations',
        'M.S. in Statistics': 'Master of Science in Data science',
        'B.S. in Mechanical Engineering in With a focs in Mechatronics':
        'Bachelor of Science in Mechanical Engineering',
        'junior architect': 'architect',
        'staff it auditor': 'auditor',
        'bachelor of arts in economics': 'bachelor of arts',
        'design and marketing director': 'marketing director',
        'it auditor': 'auditor',
        '"Bachelors in Healthcare Management/Administration"':
        'Bachelors in Administration',
        'thousands of data analysts': 'data science',
        'business analyst': 'business analyst',
        'and backend engineers': 'software engineer',
        'u"recruiter': 'recuiter',
        'bachelor of science in medical technology':
        'bachelor of science in medicine',
        'associate': 'associate',
        'vp of operations': 'vp of operations',
        'degree_2 :': '',
        'diploma': '',
        'software engineer': 'software engineer',
        'u"sales associate': 'sales',
        'bachelor of science in mechanical engineering':
        'bachelor of science in mechanical engineering',
        'high school or eqivalent': '',
        'managed and developed junior analyst': 'data science',
        'supervise recruiter': 'recruiter',
        'degree_1 :': '',
        'engineers': 'engineer',
        'b.s in fashion design': 'bachelor of science in fashion',
        'product and engineering teams': 'engineer',
        'u"senior systems engineer': 'software engineer',
        'senior revenue analyst': 'business analyst',
        'lead technical / business strategist/ dmts': 'business analyst',
        'mechanical design engineer': 'engineer',
        '"bachelors"': 'bachelor of science in mechanical engineering',
        'b.s. in electrical engineering':
        'bachelor of science in electrical engineering',
        '"Masters in Compter Science"':
        'master of science in computer science',
        'u"decision scientist': 'business analyst',
        'Bachelor of Engineering in Engineering':
        'bachelor of science in electrical engineering',
        'High School': '',
        'Bachelors of Science in Hman Resorce Management':
        'Bachelors in Administration',
        'director of engineering & facilities': 'director of engineering',
        'human resource director': 'recuiter',
        'architect / lead systems engineer': 'software engineer',
        'BS in Bsiness Administration': 'Bachelors in Administration',
        'customer system engineer / advocate': 'software engineer',
        'Bachelors in Bsiness Management"': 'Bachelors in Administration',
        "process engineering (technical services)": "process engineer",
        "b.s. in mechanical engineering in with a focs in mechatronics":
        "bachelor of science in mechanical engineering",
        "aerospace engineer (contract)": "aerospace engineer",
        "lead electromechanical engineer": "senior electromechanical engineer",
        "senior engineering manager": "senior engineer manager",
        "lead engineer & founder": "founder",
        "master in chemical engineering":
        "master of science in chemical engineering",
        "manager/assistant director": "manager",
        "associates of science in general science":
        "diploma in general science",
        "bachelor of science in engineering in indstrial engineering":
        "bachelor of science in indstrial engineering",
        "associates of applied science in compter aided drafting and design":
        "diploma in cad",
        "engineering technician iii": "technician",
        "associate of science degree in mechanical engineering":
        "diploma in mechanical engineering",
        "engineering technician": "technician",
        "engineering project manager - stores": "engineering project manager",
        "bs in civil engineering": "bachelor of science in civil engineering",
        "preparation and evalation of projects": "engineering project manager",
        "assistant and supervisor of engineering projects":
        "engineering project manager",
        "in graphic design": "bachelor of science in graphic design",
        "carpenter restorer in restoration of works of art": "carpenter",
        "bs in chemical engineering":
        "bachelor of science in chemical engineering",
        "b.s. in physics in physics": "bachelor of science in physics",
        "b.s. in mechanical engineering":
        "bachelor of science in mechanical engineering",
        "senior plant engineer": "senior engineer",
        "project manager - corporate engineering": "project manager",
        "mba in exective": "master in business administration",
        "associate (did not complete) in civil engineering":
        "diploma in civil engineering",
        "senior structural engineering technician": "senior technician",
        "bachelor of science in civil engineering in \
         fndamentals of engineering exam":
        "bachelor of science in civil engineering",
        "as in mechanical & general engineering technology":
        "bachelor of science in mechanical engineering",
        "bs in manfactring technology":
        "bachelor of science in manufacturing technology",
        "ms in organizational leadership and qality":
        "master of science in organizational leadership and qality",
        "master in compters in compters":
        "master of science in computer science",
        "sr. engineering manager": "senior engineering manager",
        "engineering / quality manager": "quality manager",
        "bachelor of science in compter science":
        "bachelor of science in computer science",
        "associates degree in compter aided design in atodesk":
        "diploma in cad",
        "a.a. in interdisciplinary stdies in interdisciplinary stdies":
        "diploma in interdisciplinary studies",
        "finance director/sales manager": "finance director",
        "associates in stationary engineering":
        "diploma in stationary engineering",
        "in teaching": "bachelor in teaching",
        "in acconting and finance": "bachelor of science in finance",
        "finance manager/director": "finance director",
        "bachelor of economics in economics": "bachelor in economics",
        "mba": "master in business administration",
        "master of bsiness administration in capital markets\
         and asset management immersion":
        "master in business administration",
        "bachelor of science in acconting":
        "bachelor of science in accounting",
        "b.a. in bsiness administration":
        "bachelor in business administration",
        "finance director/secondary director": "finance director",
        "finance director /sales manager": "finance director",
        "m.a. in conseling": "master in counseling",
        "in accounting": "bachelor of science in accounting",
        "in finance": "bachelor of science in finance",
        "associates degree/bachelor in criminal science/jstice":
        "bachelor in criminal science",
        "ba in bsiness administration": "bachelor in business administration",
        "bs in finance": "bachelor of science in finance",
        "master of bsiness administration in strategy and finance":
        "master in business administration",
        "bachelor in management/finance": "bachelor of science in finance",
        "in bsiness economics": "bachelor in economics",
        "bs and gradate work": "bachelor of science in finance",
        "usn in usn.": "bachelor of science in finance",
        "sales manager/finance director": "finance director",
        "bachelor of liberal arts and science in liberal arts and science":
        "bachelor of science in liberal arts",
        "senior financial analyst/office manager": "senior financial analyst",
        "richard m squire and associates llc - jenkintown": "associate",
        "libereal arts in compter science":
        "bachelor of science in liberal arts",
        "master in psychology and sports management/marketing":
        "master in psychology",
        "in conseling edcation": "bachelor in counseling education",
        "director of finance": "finance director",
        "bs in mechanical engineering":
        "bachelor of science in mechanical engineering",
        "bs in acconting": "bachelor of science in accounting",
        "certification in business essentials": "diploma in business",
        "business/financial analyst": "business analyst",
        "bachelor of science in finance in finance":
        "bachelor of science in finance",
        "ba in commnications": "bachelor in communications",
        "bs in economics in international economics and trade":
        "bachelor in economics",
        "master in economics in international trade": "master in economics",
        "master in acconting": "master of science in accounting",
        "b.s.": "bachelor of science in finance",
        "m.b.a.": "master in business administration",
        "bachelor of science in bsine ss":
        "bachelor in business administration",
        "in finance and real estate": "bachelor of science in finance",
        "financial analyst ii": "senior financial analyst",
        "bachelor in finance": "bachelor of science in finance",
        "master of business administration":
        "master in business administration",
        "master in finance": "master of science in finance",
        "bachelor of science in economics in economics":
        "bachelor in economics",
        "master of science in finance in information\
         technology and electronic commerce":
        "master of science in finance",
        "mba in finance": "master in business administration",
        "associates of science degree": "diploma in science",
        "bachelor of science in hman resorce management":
        "bachelor in human resource management",
        "recuiter": "recruiter",
        "bachelor of science in business administration/personnel management":
        "bachelor in business administration",
        "director of facilities management/hr": "hr director",
        "bachelor of science in business management":
        "bachelor of science in management",
        "master in hman resorces management":
        "master in human resource management",
        "human resource associate (contract)": "human resource associate",
        "master of pblic administration in pblic administration":
        "master in public administration",
        "in hman resorce management": "master in human resource management",
        "bba": "bachelor in business administration",
        "in bank": "human resource associate",
        "bachelor of arts in hman resorces":
        "bachelor in human resource management",
        "hr recruiter": "recruiter",
        "human resource recruiter - client": "recruiter",
        "bachelor of science degree in business management":
        "bachelor of science in management",
        "master degree in core": "master in human resource management",
        "bba in business administration":
        "bachelor in business administration",
        "ma in organizational management specialization hman resorces":
        "master in human resource management",
        "director of human capital": "hr director",
        "instructor/recruiter": "recruiter",
        "driver recruiter": "recruiter",
        "corporate recruiter": "recruiter",
        "associates of art business in art business": "diploma in business",
        "interim human resources director": "hr director",
        "bachelor of arts in organizational development":
        "bachelor of science in organizational leadership",
        "master of science in organizational leadership":
        "master of science in organizational leadership",
        "bachelor in bsiness administration":
        "bachelor in business administration",
        "director of human resources": "hr director",
        "master in hman resorces development":
        "master in human resource management",
        "in bsiness administration and management":
        "bachelor in business administration",
        "mba in bsiness administration": "master in business administration",
        "n master of bsiness administration":
        "master in business administration",
        "bs in bsiness management": "bachelor of science in management",
        "in hman resorce certification": "diploma in human resource",
        "in general stdies": "bachelor in general studies",
        "director of talent management": "hr director",
        "director human resources": "hr director",
        "a.a.s. in bsiness": "diploma in business",
        "ba in sociology": "bachelor of arts in sociology",
        "raskin & associates": "associate",
        "associate of science in bsiness": "diploma in business",
        "manager/marketing director": "marketing director",
        "activities director / marketing director": "marketing director",
        "community admissions & marketing director": "marketing director",
        "activities director/ recovery coach / marketing":
        "marketing director",
        "associates of science in marketing": "diploma in marketing",
        "bachelor of science in marketing": "bachelor of science in marketing",
        "bachelor of science in bsiness and economics":
        "bachelor in economics",
        "bachelor of arts in commnication stdies":
        "bachelor in communications",
        "bachelor of science in bsiness administration":
        "bachelor in business administration",
        "bachelor of arts in american stdies":
        "bachelor of arts in american studies",
        "director of marketing": "marketing director",
        "marketing director/consultant": "marketing director",
        "in english literatre": "bachelor of arts in english literatre",
        "bachelors of science": "bachelor of science",
        "bs in marketing": "bachelor of science in marketing",
        "master of pblic administration in m health information systems":
        "master in public administration",
        "bachelor of arts in marketing management & pblic relations":
        "bachelor of science in marketing",
        "bba in marketing": "bachelor of science in marketing",
        "in sales": "bachelor in sales",
        "associate of arts in telecommnications in telecommnications":
        "diploma in telecommunications",
        "bachelor of arts in mass commnications in pblic relation":
        "bachelor in communications",
        "masters of science in hman services \
        administration in overall gradate":
        "master in human resource management",
        "marketing director/administrator": "marketing director",
        "bachelor of science in c technology":
        "bachelor of science in indstrial engineering",
        "bachelor of business administration in finance/economics":
        "bachelor in business administration",
        "sr. financial analyst": "senior financial analyst",
        "bachelor of science in corporate finance/ business management":
        "bachelor of science in finance",
        "bachelor of arts in business administration":
        "bachelor in business administration",
        "master of business administration in deloitte technology":
        "master in business administration",
        "master of science in finance in information\
        technology and electronic commerce":
        "master of science in finance",
        "bachelor in business administration in\
        finance in business administration":
        "bachelor in business administration",
        "senior financial analyst (consultant)":
        "senior financial analyst",
        "senior financial planning analyst": "senior financial analyst",
        "master in finance in finance": "master of science in finance",
        "bachelor of science in business administration\
        in business administration":
        "bachelor of science in business",
        "business data analyst": "business analyst",
        "masters in business administration":
        "master in business administration",
        "bachelor of business administration in corporate finance":
        "bachelor in business administration",
        "bachelor of business administration in finance":
        "bachelor in business administration",
        "bachelor in business administration finance":
        "bachelor in business administration",
        "ma in theology and biblical stdies":
        "master in theology and biblical studies",
        'bachelor of science in business administration':
        "bachelo in business administration",
        "master in business administration w/ concentration\
        in lean manfactring":
        "master in business administration",
        "masters of science in lean manfactring in operations management":
        "master of science in operations management",
        "ms-mechanical engineering in msme":
        "master of science in mechanical engineering",
        "research analyst/assistant": "research analyst",
        "ph.d. in mechanical engineering": "phd in mechanical engineering",
        "bachelor of science in mechanical engineering program":
        "bachelor of science in mechanical engineering",
        "bse in mechanical": "bachelor of science in mechanical engineering",
        'master in mechanical engineering':
        'master of science in mechanical engineering',
        "engineering manager/proposal manager": "engineer manager",
        "engineering manager/sales": "engineer manager",
        "in civil engineering gradate":
        "bachelor of science in civil engineering",
        "engineering field technician/ inspector": "technician",
        "bachelor of science in mechanical engineering\
        technology and prodct design":
        "bachelor of science in mechanical engineering",
        "manager engineering": "engineer manager",
        "bachelor of science in mechanical engineering\
        in mechanical engineering":
        "bachelor of science in mechanical engineering",
        "bachelor of science degree in engineering":
        "bachelor of science in engineering",
        "tech/maint. supv./plant engineer": "plant engineer",
        "plant engineering manager": "plant engineer manager",
        "mechanical engineering team manager": "engineer manager",
        "engineering and manufacturing technician": "technician",
        "in business administration": "bachelor in business administration",
        "bachelor of science in psychology in psychology":
        "bachelor of science in psychology",
        "finance controller/director of finance": "finance director",
        "bachelor in commnications": "bachelor in communications",
        "director/finance manager": "finance manager",
        "business and management": "bachelor in business administration",
        "finance director/ manager": "finance director",
        "post in business administration": "master in business administration",
        "bachelor of business administration in business administration":
        "bachelor in business administration",
        "m.b.a. in faclty": "master in business administration",
        "b.s. in business administration and finance":
        "bachelor in business administration",
        "associate of science in business administration":
        "diploma in business administration",
        "certificate in hman resorce management":
        "certificate in human resource management",
        "bachelor of science in business\
        administration/hman resorce management":
        "bachelor in business administration",
        "degree in administration": "diploma in business administration",
        "bs in hman resorces": "bachelor in human resource management",
        "achelor of arts in hman resorce management":
        "bachelor in human resource management",
        "master in organizational development":
        "master of science in organizational leadership",
        "certification in advanced hman capital management":
        "certification in human resource management",
        "m.s. in hman resorce management":
        "master in human resource management",
        "regional director of human resources": "hr director",
        "bachelor of science in business administration":
        "bachelor in business administration",
        "certificate in administration & finance":
        "certificate in business administration",
        "associate in applied science in airline\
        and secretarial administration":
        "diploma in applied science",
        "human resources director": "hr director",
        "administrative assistant/ hr associate": "hr associate",
        "b.s in business administration sbject":
        "bachelor in business administration",
        "human resource manager/safety director": "human resource manager",
        "bachelor of arts in hman resorce management":
        "bachelor in human resource management",
        "bachelor in business/hman resorces":
        "bachelor in human resource management",
        "certification in human resource management":
        "certificate in human resource management",
        "human resource recruiter": "recruiter",
        "certification": "certificate",
        "bachelor of business administration in hman resorce management":
        "bachelor in human resource management",
        "bachelor of science in mass commnications":
        "bachelor in communications",
        "associate in jornalism/mass commnications":
        "diploma in communication",
        "sr. marketing director": "senior marketing director",
        "bachelor in emerging media and commnications":
        "bachelor in communications",
        "b.s. in marketing": "bachelor of science in marketing",
        "director marketing": "marketing director",
        "bachelor of business administration in marketing":
        "bachelor in business administration",
        "optical stylist/marketing directo": "marketing director",
        "bachelor in international marketing":
        "bachelor of science in marketing",
        "ba in graphic commnication": "bachelor in communications",
        "art director/designer": "art director",
        "bachelor of science in business in marketing":
        "bachelor of science in marketing",
        "community relations & marketing director": "marketing director",
        "director - sales and marketing": "marketing director",
        "optical stylist/marketing director": "marketing director",
        "associate of arts in psychology in psychology":
        "diploma in psychology",
        "events & marketing director": "marketing director",
        "senior financial analyst/financial analyst": "financial analyst",
        "bachelor of science in business administration in finance":
        "bachelor in business administration",
        "b.s.b.a. in finance in finance": "bachelor of science in finance",
        "lead financial analyst": "senior financial analyst",
        "bachelor of economics in labor and social economics":
        "bachelor in economics",
        "b.a. in acconting": "bachelor of science in accounting",
        "b.s. in finance in finance": "bachelor of science in finance",
        "ba science": "bachelor in science",
        "mba in health care administration":
        "master in business administration",
        "financial analyst/intern": "intern"}

    if current in nodes and aim in nodes:
        source = current
        target = aim

    elif current in mapping and aim in nodes:
        source = mapping[current]
        target = aim

    elif current in nodes and aim in mapping:
        source = current
        target = mapping[aim]

    elif current in mapping and aim in mapping:
        source = mapping[current]
        target = mapping[aim]

    else:
        source = current
        target = aim

    return source, target


def current_and_aim(current, aim, weight=None):

    graph_most_common = nx.read_gpickle('../../Data/graphs/\
                                        final_graphs/most_common')
    graph_min_transitions = nx.read_gpickle('../../Data/graphs/\
                                            final_graphs/min_transitions')
    graph_min_time = nx.read_gpickle('../../Data/graphs/final_graphs\
                                        /shortest_time')
    graph_combination = nx.read_gpickle('../../Data/graphs/final_graphs\
                                        /combination')

    source, target = transform_function(current, aim, graph_most_common)

    try:
        if weight == "most common":
            return nx.dijkstra_path(graph_most_common, source, target)

        elif weight == "minimum transitions":
            return nx.dijkstra_path(graph_min_transitions, source, target)

        elif weight == "minimum time":
            return nx.dijkstra_path(graph_min_time, source, target)

        elif weight == "combination":
            return nx.dijkstra_path(graph_combination, source, target)

        else:
            return k_shortest_paths_default(graph_most_common,
                                            source, target, 3)

    except (ValueError, TypeError, OSError):
        return "Wrong Input"
