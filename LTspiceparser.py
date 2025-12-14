

#   ========== SENparser ==========
#   EN hurtig og slem parser til
#   LTspice output logs.
#   Måske / Måske ikke med hints
#   til nogle katte der skriger 
#   
#   Skrevet af yours truely
#   Malther SENnels


def file_fetch(Path: str):
    file = open(Path, "r")
    lines = file.readlines()
    file.close()
    return lines #Bum hurtig og smertefrit så har vi alle linjer tekst til at gå igennem





def file_get_meas(Name: str, lines: list[str]):
    """Løber igennem listen finder det sted der står vores meas og returnerer en liste med de værdier den har givet"""

    index = -1
    for n in range(0, len(lines)):
        if(lines[n].find("Measurement:") == -1):
            continue
        if(lines[n].strip().lower().find(Name.lower()) == -1):
            continue
        #hvis vi nået hertil så har vi fundet de linjer vi skal bruge
        index = n
        break
    if(index == -1):
        raise Exception("[Kat der srkiger]: Kunne ikke finde {} .meas variabel i filen".format(Name))
    

    results = []
    for i in range(n+2, len(lines)): #Vi scroller igennem listen af målinger
        colums = lines[i].split("\t")
        if (not colums[0].strip().isnumeric()): #Hvis der ikke er tal i det vi kigger på så det fordi vi har ramt enden
            break
        results.append(float(colums[1]))
    return results


def file_get_step(Name: str, lines: list[str]):
    """Henter den aktuelle step param værdi ud fra output loggen.  """


    output = []
    for n in range(0, len(lines)):
        if(lines[n].find(".step") == -1):
            continue
        #hvis vi nået hertil så har vi fundet de linjer vi skal bruge
        index = lines[n].find(Name.lower())
        if (index == -1):
            continue
        
        argument = lines[n][index:].split("=")[1].split(" ")[0]
        ##Så skal vi filtrerer lidt på det
        argument = argument.replace('°C', "").rstrip() ##Hvis vi arbejder i grader
        output.append(float(argument))

        
    if(len(output) == 0): ##Listen er tom så der nok gået noget galt
        raise Exception("[Kat der srkiger]: Kunne ikke finde {}= .step variabel i filen".format(Name))
    
    return output

def file_get_THD(Name: str, lines: list[str]):
    """Finder THD'erne i %"""

    output_total = []
    for n in range(0, len(lines)):
        if(lines[n].find("Fourier components of ") == -1):
            continue
        if(lines[n].split(" ")[-1].rstrip().lower() != Name.lower()):
            continue
        #hvis vi nået hertil så har vi fundet de linjer vi skal bruge
        
        for i in range(n, len(lines)): ##SÅ sprinter vi lige ned i bunden af tabellen og hiver det første THD ud
            if(lines[i].find("Total Harmonic Distortion:") == -1):
                continue
            ##Her har vi fundet den linje hvor THD'en står
            output_total.append(float(lines[i].split(" ")[-1].replace("%", ""))) ##Vi hapser lige den THD vi skal bruge
            break

    if(len(output_total) == 0): ##Listen er tom så der nok gået noget galt
        raise Exception("[Kat der srkiger]: Kunne ikke finde {} som en .fourier".format(Name))
    
    return output_total




if __name__ == "__main__":
    print("Starter pisset")
    lines = file_fetch("CA_Together.log")  

    temps = file_get_step("temp", lines)



