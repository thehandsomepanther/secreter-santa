from ff import *
import json

def main():
    g = FlowNetwork()
    g.add_vertex('s')
    g.add_vertex('t')

    A = []
    B = []

    with open('santa.json') as json_file:
        data = json.load(json_file)
        last_year = 0

        for person in data:
            years = []

            for key in data[person]["matches"].keys():
                years.append(int(key))

            last_year = max(last_year, max(years))

            person_a = person + "_A"
            g.add_vertex(person_a)
            g.add_edge('s', person_a, 100)
            A.append(person_a)

            person_b = person + "_B"
            g.add_vertex(person_b)
            g.add_edge(person_b, 't', 100)
            B.append(person_b)

        for person_a in A:
            for person_b in B:
                flow = 100
                if person_a[:-2] != person_b[:-2]:
                    if data[person_a[:-2]]["matches"][str(last_year - 1)] != person_b[:-2]:
                        for key in data[person_a[:-2]]["matches"].keys():
                            repeats = 1
                            if data[person_a[:-2]]["matches"][key] == person_b[:-2]:
                                repeats += 1
                            flow = flow / repeats
                    else:
                        flow = 0
                else:
                    flow = 0

                g.add_edge(person_a, person_b, flow)
                print "{}-{}->{}".format(person_a, flow, person_b)


    print g.max_flow('s', 't')

main()
