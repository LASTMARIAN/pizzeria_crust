from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Pizzat, Juomat, Asiakas, Tilausrivi, Tilaus

tilaus_common = []
asiakkaat = Asiakas.objects.values_list()
koko_hinta = 0
def application(request):
    

    return render(request, "application.html")

def checkout(request):
    global koko_hinta
    global tilaus_common
    tilaus_common.clear()
    local_koko_hinta = 0
    koko_hinta = 0
    
    pizza_dict = {
        1 : [request.POST.get("input1_p"), request.POST.get("koko1")],
        2 : [request.POST.get("input2_p"), request.POST.get("koko2")],
        3 : [request.POST.get("input3_p"), request.POST.get("koko3")],
        4 : [request.POST.get("input4_p"), request.POST.get("koko4")], 
        5 : [request.POST.get("input5_p"), request.POST.get("koko5")], 
        6 : [request.POST.get("input6_p"), request.POST.get("koko6")],
        7 : [request.POST.get("input7_p"), request.POST.get("koko7")], 
        8 : [request.POST.get("input8_p"), request.POST.get("koko8")], 
        9 : [request.POST.get("input9_p"), request.POST.get("koko9")]
    }

    koko_dict = {
        "S" : 2,
        "M" : 1,
        "L" : 0
    }
     
    juoma_array = [
        request.POST.get("input1_j"), request.POST.get("input2_j"), 
        request.POST.get("input3_j"), request.POST.get("input4_j"), 
        request.POST.get("input5_j"), request.POST.get("input6_j"), 
        request.POST.get("input7_j"), request.POST.get("input8_j"), 
        request.POST.get("input9_j"), request.POST.get("input10_j")
    ]

    tilaus = []

    for each in range(1, len(pizza_dict) + 1):
        if (pizza_dict[each][0] != "0"):
            record = Pizzat.objects.get(pizza_id = each * 3 - koko_dict[pizza_dict[each][1]])  
            tilaus.append([record.nimi, pizza_dict[each][1], int(record.hinta) * int(pizza_dict[each][0]), pizza_dict[each][0]]) 
            local_koko_hinta += int(pizza_dict[each][0]) * record.hinta

    for each in juoma_array:
        if each != "0":
            record = Juomat.objects.get(juoma_id = juoma_array.index(each) + 1)
            tilaus.append([record.juoma_id, record.nimi, int(record.hinta) * int(each), each]) 
            local_koko_hinta += record.hinta * int(each)
    for each in tilaus:
        tilaus_common.append(each)
    
    koko_hinta += local_koko_hinta
    data = {"tilaus" : tilaus, "local_koko_hinta" : koko_hinta}
    return render(request, "checkout.html", context=data)

def success(request):
    global asiakkaat
    global koko_hinta
    global tilaus_common
    is_failed = False
    username_coincidence = 0
    username_id = 0
    for each in asiakkaat:
        if each[1] == request.POST.get("username") and each[2] == request.POST.get("password"):
            username_coincidence += 1
            username_id = each[0]

    if username_coincidence == 1:
        Tilaus.objects.create(asiakas=Asiakas.objects.get(asiakas_id=username_id), hinta=koko_hinta)

        for each in range(0, len(tilaus_common)):
            if (len(tilaus_common[each][1]) == 1):
                record = Pizzat.objects.get(nimi=tilaus_common[each][0], koko=tilaus_common[each][1]) 
                Tilausrivi.objects.create(pizza=record, juoma=None, pizzamaara=tilaus_common[each][3], tilaus=Tilaus.objects.last(), juomamaara=0, hintapizzarivi=tilaus_common[each][2], hintajuomarivi=0)
            else:
                record = Juomat.objects.get(juoma_id=tilaus_common[each][0])
                Tilausrivi.objects.create(pizza=None, juoma=record, pizzamaara=0, juomamaara=tilaus_common[each][3], tilaus=Tilaus.objects.last(), hintapizzarivi=0, hintajuomarivi=tilaus_common[each][2])
        
        
        return render(request, "success.html")

        
    if username_coincidence == 0:
        is_failed = True
        data = {"is_failed" : is_failed, "tilaus" : tilaus_common, "local_koko_hinta" : koko_hinta}
        return render(request, "checkout.html", context=data)

def registration(request):
    if_registered = False
    if_length = False
    käyttäjätunnus = request.POST.get("username")
    asiakas_list = Asiakas.objects.values_list()
    if käyttäjätunnus == None:

        return render(request, "registration.html")
    else:
        if (len(request.POST.get("username")) > 0 and len(request.POST.get("password")) > 0 and len(request.POST.get("name")) > 0
            and len(request.POST.get("phone")) > 0 and len(request.POST.get("email")) > 0 and len(request.POST.get("address")) > 0):
            coincidence = 0
            for each in asiakas_list:
                if (each[1] == request.POST.get("username")):
                    coincidence += 1
                    if_registered = True
                    data = {"if_registered" : if_registered, "if_length" : if_length}
                    return render(request, "registration.html", context=data)
                    
            if coincidence == 0:
                Asiakas.objects.create(username=request.POST.get("username"), password=request.POST.get("password"), nimi=request.POST.get("name"),
                                    puhnumero=request.POST.get("phone"), sahkoposti=request.POST.get("email"), osoite=request.POST.get("address"))
                return render(request, "registration_success.html")
        else:
            if_length = True
            data = {"if_registered" : if_registered, "if_length" : if_length}
            return render(request, "registration.html", context=data)
