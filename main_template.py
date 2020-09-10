#
# Podstawy Sztucznej Inteligencji, IIS 2020
# Autor: Tomasz Jaworski
# Opis: Szablon kodu do stabilizacji odwróconego wahadła (patyka) w pozycji pionowej podczas ruchu wózka.
#

import gym # Instalacja: https://github.com/openai/gym
import time
from helper import HumanControl, Keys, CartForce, RealDomains, Ops
import matplotlib.pyplot as plt
from defaults import Force, Distance, Angle, Velocity, AngleVelocity
#
# przygotowanie środowiska
#
control = HumanControl()
domains = RealDomains()
env = gym.make('gym_PSI:CartPole-v2')
env.reset()
env.render()
desired_position = 0.0
task2 = False
def on_key_press(key: int, mod: int):
    global control
    global desired_position
    force = 10
    if key == Keys.LEFT:
        if control.WantPause:
            desired_position = desired_position - 0.5 if desired_position >= -2.0 else -2.5
        else:
            control.UserForce = force * CartForce.UNIT_LEFT # krok w lewo
    if key == Keys.RIGHT:
        if control.WantPause:
            desired_position = desired_position + 0.5 if desired_position <= 2.0 else 2.5
        else:
            control.UserForce = force * CartForce.UNIT_RIGHT # krok w prawo
    if key == Keys.P: # pauza
        control.WantPause = ~control.WantPause
    if key == Keys.R: # restart
        control.WantReset = True
    if key == Keys.ESCAPE or key == Keys.Q: # wyjście
        control.WantExit = True

env.unwrapped.viewer.window.on_key_press = on_key_press

#########################################################
# KOD INICJUJĄCY - do wypełnienia
#########################################################

"""

1. Określ dziedzinę dla każdej zmiennej lingwistycznej. Każda zmienna ma własną dziedzinę.
2. Zdefiniuj funkcje przynależności dla wybranych przez siebie zmiennych lingwistycznych.
3. Wyświetl je, w celach diagnostycznych.

Przykład wyświetlania:

fig, (ax0) = plt.subplots(nrows=1, figsize=(8, 9))

ax0.plot(x_variable, variable_left, 'b', linewidth=1.5, label='Left')
ax0.plot(x_variable, variable_zero, 'g', linewidth=1.5, label='Zero')
ax0.plot(x_variable, variable_right, 'r', linewidth=1.5, label='Right')
ax0.set_title('Angle')
ax0.legend()


plt.tight_layout()
plt.show()
"""

fuzzy_cart_force_signal = Ops.GenerateFuzzyMemberships(domains.CartForces, High=Force.HighVec, MidHigh=Force.MidHighVec,
                                                       Mid=Force.MidVec, MidLight=Force.MidLightVec, Light=Force.LightVec,
                                                       Idle=Force.IdleVec,LightNegative=sorted([-x for x in Force.LightVec]),
                                                       MidLightNegative=sorted([-x for x in Force.MidLightVec]),
                                                       MidNegative=sorted([-x for x in Force.MidVec]),
                                                       MidHighNegative=sorted([-x for x in Force.MidHighVec]),
                                                       HighNegative=sorted([-x for x in Force.HighVec]))
                                                       
fuzzy_cart_distance_signal = Ops.GenerateFuzzyMemberships(domains.CartPositions, Far=Distance.FarVec, MidFar=Distance.MidFarVec,
                                                          Mid=Distance.MidVec, Close=Distance.CloseVec, InPlace=Distance.InPlaceVec,
                                                          CloseNegative=sorted([-x for x in Distance.CloseVec]),
                                                          MidNegative=sorted([-x for x in Distance.MidVec]),
                                                          MidFarNegative=sorted([-x for x in Distance.MidFarVec]),
                                                          FarNegative=sorted([-x for x in Distance.FarVec]))

fuzzy_pendulum_angle_signal = Ops.GenerateFuzzyMemberships(domains.PendulumAngles, Large=Angle.LargeVec, MidLarge=Angle.MidLargeVec,
                                                           Mid=Angle.MidVec, Small=Angle.SmallVec, Zero=Angle.ZeroVec,
                                                           SmallNegative=sorted([-x for x in Angle.SmallVec]), MidNegative=sorted([-x for x in Angle.MidVec]),
                                                           MidLargeNegative=sorted([-x for x in Angle.MidLargeVec]), LargeNegative=sorted([-x for x in Angle.LargeVec]))

fuzzy_cart_velocity_signal = Ops.GenerateFuzzyMemberships(domains.CartVelocities, High=Velocity.HighVec, Mid=Velocity.MidVec, Small=Velocity.SmallVec,
                                                          Idle=Velocity.IdleVec, SmallNegative=sorted([-x for x in Velocity.SmallVec]),
                                                          MidNegative=sorted([-x for x in Velocity.MidVec]), HighNegative=sorted([-x for x in Velocity.HighVec]))

fuzzy_tip_velocity_signal = Ops.GenerateFuzzyMemberships(domains.PendulumVelocities, High=AngleVelocity.HighVec, Mid=AngleVelocity.MidVec,
                                                         Small=AngleVelocity.SmallVec, Idle=AngleVelocity.IdleVec, SmallNegative=sorted([-x for x in AngleVelocity.SmallVec]),
                                                         MidNegative=sorted([-x for x in AngleVelocity.MidVec]), HighNegative=sorted([-x for x in AngleVelocity.HighVec]))

#########################################################
# KONIEC KODU INICJUJĄCEGO
#########################################################


#
# Główna pętla symulacji
#
while not control.WantExit:

    #
    # Wstrzymywanie symulacji:
    # Pierwsze wciśnięcie klawisza 'p' wstrzymuje; drugie wciśnięcie 'p' wznawia symulację.
    #
    if control.WantPause:
        
        while control.WantPause:
            time.sleep(0.5)
            env.render()
        control.WantPause = False

    #
    # Czy użytkownik chce zresetować symulację?
    if control.WantReset:
        control.WantReset = False
        env.reset()


    ###################################################
    # ALGORYTM REGULACJI - do wypełnienia
    ##################################################

    """
    Opis wektora stanu (env.state)
        cart_position   -   Położenie wózka w osi X. Zakres: -2.5 do 2.5. Ppowyżej tych granic wózka znika z pola widzenia.
        cart_velocity   -   Prędkość wózka. Zakres +- Inf, jednak wartości powyżej +-2.0 generują zbyt szybki ruch.
        pole_angle      -   Pozycja kątowa patyka, a<0 to odchylenie w lewo, a>0 odchylenie w prawo. Pozycja kątowa ma
                            charakter bezwzględny - do pozycji wliczane są obroty patyka.
                            Ze względów intuicyjnych zaleca się konwersję na stopnie (+-180).
        tip_velocity    -   Prędkość wierzchołka patyka. Zakres +- Inf. a<0 to ruch przeciwny do wskazówek zegara,
                            podczas gdy a>0 to ruch zgodny z ruchem wskazówek zegara.
                            
    Opis zadajnika akcji (fuzzy_response):
        Jest to wartość siły przykładana w każdej chwili czasowej symulacji, wyrażona w Newtonach.
        Zakładany krok czasowy symulacji to env.tau (20 ms).
        Przyłożenie i utrzymanie stałej siły do wózka spowoduje, że ten będzie przyspieszał do nieskończoności,
        ruchem jednostajnym.
    """

    cart_position, cart_velocity, pole_angle, tip_velocity = env.state # Wartości zmierzone
    

    """
    
    1. Przeprowadź etap rozmywania, w którym dla wartości zmierzonych wyznaczone zostaną ich przynależności do poszczególnych
       zmiennych lingwistycznych. Jedno fizyczne wejście (źródło wartości zmierzonych, np. położenie wózka) posiada własną
       zmienną lingwistyczną.
       
       Sprawdź funkcję interp_membership
       
    2. Wyznacza wartości aktywacji reguł rozmytych, wyznaczając stopień ich prawdziwości.
       Przykład reguły:
       JEŻELI kąt patyka jest zerowy ORAZ prędkość wózka jest zerowa TO moc chwilowa jest zerowa
       JEŻELI kąt patyka jest lekko ujemny ORAZ prędkość wózka jest zerowa TO moc chwilowa jest lekko ujemna
       JEŻELI kąt patyka jest średnio ujemny ORAZ prędkość wózka jest lekko ujemna TO moc chwilowa jest średnio ujemna
       JEŻELI kąt patyka jest szybko rosnący w kierunku ujemnym TO moc chwilowa jest mocno ujemna
       .....
       
       Przyjmując, że spójnik LUB (suma rozmyta) to max() a ORAZ/I (iloczyn rozmyty) to min() sprawdź funkcje fmax i fmin.
    
    
    3. Przeprowadź agregację reguł o tej samej konkluzji.
       Jeżeli masz kilka reguł, posiadających tę samą konkluzję (ale różne przesłanki) to poziom aktywacji tych reguł
       należy agregować tak, aby jedna konkluzja miała jeden poziom aktywacji. Skorzystaj z sumy rozmytej.
    
    4. Dla każdej reguły przeprowadź operację wnioskowania Mamdaniego.
       Operatorem wnioskowania jest min().
       Przykład: Jeżeli lingwistyczna zmienna wyjściowa ForceToApply ma 5 wartości (strong left, light left, idle, light right, strong right)
       to liczba wyrażeń wnioskujących wyniesie 5 - po jednym wywołaniu operatora Mamdaniego dla konkluzji.
       
       W ten sposób wyznaczasz aktywacje poszczególnych wartości lingwistycznej zmiennej wyjściowej.
       Uważaj - aktywacja wartości zmiennej lingwistycznej w konkluzji to nie liczba a zbiór rozmyty.
       Ponieważ stosujesz operator min(), to wynikiem będzie "przycięty od góry" zbiór rozmyty. 
       
    5. Agreguj wszystkie aktywacje dla danej zmiennej wyjściowej.
    
    6. Dokonaj defuzyfikacji (np. całkowanie ważone - centroid).
    
    7. Czym będzie wyjściowa wartość skalarna?
    
    """


    fuzzy_response = CartForce.IDLE_FORCE # do zmiennej fuzzy_response zapisz wartość siły, jaką chcesz przyłożyć do wózka.
    
    #signal activations
    fuzzy_cart_distance_signal_activations = Ops.GetRules(fuzzy_cart_distance_signal, domains.CartPositions, desired_position - cart_position)
    fuzzy_cart_velocity_signal_activations = Ops.GetRules(fuzzy_cart_velocity_signal, domains.CartVelocities, cart_velocity)
    fuzzy_pendulum_angle_signal_activations = Ops.GetRules(fuzzy_pendulum_angle_signal, domains.PendulumAngles, pole_angle)
    fuzzy_tip_velocity_signal_activations = Ops.GetRules(fuzzy_tip_velocity_signal, domains.PendulumVelocities, tip_velocity)
    
    
    
    
    #define thesis
    idle_force_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_Large"], fuzzy_tip_velocity_signal_activations["is_HighNegative"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_LargeNegative"], fuzzy_tip_velocity_signal_activations["is_High"]),)
    #left
    mid_left_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_MidNegative"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidNegative"], fuzzy_tip_velocity_signal_activations["is_Idle"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidNegative"], fuzzy_tip_velocity_signal_activations["is_SmallNegative"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_SmallNegative"], fuzzy_tip_velocity_signal_activations["is_SmallNegative"]))
    mid_high_left_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_HighNegative"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidLargeNegative"], fuzzy_tip_velocity_signal_activations["is_Idle"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidNegative"], fuzzy_tip_velocity_signal_activations["is_MidNegative"]),)
    mid_light_left_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_SmallNegative"]))
    high_left_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_LargeNegative"], fuzzy_tip_velocity_signal_activations["is_SmallNegative"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidLargeNegative"], fuzzy_tip_velocity_signal_activations["is_MidNegative"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_SmallNegative"], fuzzy_tip_velocity_signal_activations["is_HighNegative"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidNegative"], fuzzy_tip_velocity_signal_activations["is_MidNegative"]),)
    light_left_thesis = Ops.And(fuzzy_pendulum_angle_signal_activations["is_SmallNegative"], fuzzy_tip_velocity_signal_activations["is_Idle"])
    
    
    #right
    mid_right_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Mid"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_Mid"], fuzzy_tip_velocity_signal_activations["is_Idle"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_Mid"], fuzzy_tip_velocity_signal_activations["is_Small"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_Small"], fuzzy_tip_velocity_signal_activations["is_Small"]))
    mid_high_right_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_High"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidLarge"], fuzzy_tip_velocity_signal_activations["is_Idle"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_Mid"], fuzzy_tip_velocity_signal_activations["is_Mid"]),)
    mid_light_right_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Small"]))
    high_right_thesis = Ops.Aggregate(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Large"], fuzzy_tip_velocity_signal_activations["is_Small"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_MidLarge"], fuzzy_tip_velocity_signal_activations["is_Mid"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_Small"], fuzzy_tip_velocity_signal_activations["is_High"]),
                                      Ops.And(fuzzy_pendulum_angle_signal_activations["is_Mid"], fuzzy_tip_velocity_signal_activations["is_Mid"]),)
    light_right_thesis = Ops.And(fuzzy_pendulum_angle_signal_activations["is_Small"], fuzzy_tip_velocity_signal_activations["is_Idle"])
    
    
    #cart desired postion stabilization
    if not task2:
        idle_force_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]), Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_InPlace"], fuzzy_cart_velocity_signal_activations["is_Idle"]), 
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_FarNegative"], fuzzy_cart_velocity_signal_activations["is_High"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Far"], fuzzy_cart_velocity_signal_activations["is_HighNegative"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Close"], fuzzy_cart_velocity_signal_activations["is_SmallNegative"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_CloseNegative"], fuzzy_cart_velocity_signal_activations["is_Small"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_MidNegative"], fuzzy_cart_velocity_signal_activations["is_Mid"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Mid"], fuzzy_cart_velocity_signal_activations["is_MidNegative"])))
        
        high_right_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]),Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_MidFarNegative"], fuzzy_cart_velocity_signal_activations["is_HighNegative"])))
        
        high_left_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]),Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_MidFar"], fuzzy_cart_velocity_signal_activations["is_High"])))
        
        mid_high_right_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]),Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_MidFarNegative"], fuzzy_cart_velocity_signal_activations["is_MidNegative"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_CloseNegative"], fuzzy_cart_velocity_signal_activations["is_HighNegative"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_InPlace"], fuzzy_cart_velocity_signal_activations["is_HighNegative"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_MidNegative"], fuzzy_cart_velocity_signal_activations["is_HighNegative"])))
        
        mid_high_left_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]),Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_MidFar"], fuzzy_cart_velocity_signal_activations["is_Mid"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Close"], fuzzy_cart_velocity_signal_activations["is_High"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_InPlace"], fuzzy_cart_velocity_signal_activations["is_High"]),
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Mid"], fuzzy_cart_velocity_signal_activations["is_High"])))
        
        mid_right_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]), Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_CloseNegative"], fuzzy_cart_velocity_signal_activations["is_MidNegative"])))
        mid_left_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]), Ops.Aggregate( 
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Close"], fuzzy_cart_velocity_signal_activations["is_Mid"])))
        
        light_right_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]), Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_CloseNegative"], fuzzy_cart_velocity_signal_activations["is_Idle"]), 
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_InPlace"], fuzzy_cart_velocity_signal_activations["is_SmallNegative"]), ))
        light_left_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]),Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Close"], fuzzy_cart_velocity_signal_activations["is_Idle"]), 
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_InPlace"], fuzzy_cart_velocity_signal_activations["is_Small"]), ))
        
        mid_light_right_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]), Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_CloseNegative"], fuzzy_cart_velocity_signal_activations["is_Mid"])))
        mid_light_left_thesis1 = Ops.And(Ops.And(fuzzy_pendulum_angle_signal_activations["is_Zero"], fuzzy_tip_velocity_signal_activations["is_Idle"]),Ops.Aggregate(
                                     Ops.And(fuzzy_cart_distance_signal_activations["is_Close"], fuzzy_cart_velocity_signal_activations["is_MidNegative"])))
        
        idle_force_thesis = Ops.Aggregate(idle_force_thesis, idle_force_thesis1)
        light_left_thesis = Ops.Aggregate(light_left_thesis, light_left_thesis1)
        light_right_thesis = Ops.Aggregate(light_right_thesis, light_right_thesis1)
        mid_light_left_thesis = Ops.Aggregate(mid_light_left_thesis1, mid_light_left_thesis)
        mid_light_right_thesis = Ops.Aggregate(mid_light_right_thesis, mid_light_right_thesis1)
        mid_left_thesis = Ops.Aggregate(mid_left_thesis, mid_left_thesis1)
        mid_right_thesis = Ops.Aggregate(mid_right_thesis1, mid_right_thesis)
        mid_high_left_thesis = Ops.Aggregate(mid_high_left_thesis, mid_high_left_thesis1)
        mid_high_right_thesis = Ops.Aggregate(mid_high_right_thesis, mid_high_right_thesis1)
        high_left_thesis = Ops.Aggregate(high_left_thesis, high_left_thesis1)
        high_right_thesis = Ops.Aggregate(high_right_thesis, high_right_thesis1)
    #conclusions
    idle_conclusion = Ops.Conclude(idle_force_thesis, fuzzy_cart_force_signal["Idle"])
    
    mid_left_conclusion = Ops.Conclude(mid_left_thesis, fuzzy_cart_force_signal["MidNegative"])
    high_left_conclusion = Ops.Conclude(high_left_thesis, fuzzy_cart_force_signal["HighNegative"])
    mid_high_left_conclusion = Ops.Conclude(mid_high_left_thesis, fuzzy_cart_force_signal["MidHighNegative"])
    light_left_conclusion = Ops.Conclude(light_left_thesis, fuzzy_cart_force_signal["LightNegative"])
    mid_light_left_conclusion = Ops.Conclude(mid_light_left_thesis, fuzzy_cart_force_signal["MidLightNegative"])
    
    mid_right_conclusion = Ops.Conclude(mid_right_thesis, fuzzy_cart_force_signal["Mid"])
    high_right_conclusion = Ops.Conclude(high_right_thesis, fuzzy_cart_force_signal["High"])
    mid_high_right_conclusion = Ops.Conclude(mid_high_right_thesis, fuzzy_cart_force_signal["MidHigh"])
    light_right_conclusion = Ops.Conclude(light_right_thesis, fuzzy_cart_force_signal["Light"])
    mid_light_right_conclusion = Ops.Conclude(mid_light_right_thesis, fuzzy_cart_force_signal["MidLight"])
    


    #aggregate conclusions
    aggregated_conclusions = Ops.Aggregate(idle_conclusion, mid_left_conclusion,
                                           mid_right_conclusion, high_left_conclusion,
                                           high_right_conclusion, mid_high_right_conclusion,
                                           light_left_conclusion, light_right_conclusion,
                                           mid_light_left_conclusion, mid_light_right_conclusion,
                                           mid_high_left_conclusion)
    
    # fig, (ax0) = plt.subplots(nrows=1, figsize=(8, 9))

    # ax0.plot(domains.CartForces, aggregated_conclusions, 'b', linewidth=1.5, label='Left')
    # ax0.set_title('Force')
    # ax0.legend()

    # plt.tight_layout()
    # plt.show()
    
    #defuzzy
    try:
        fuzzy_response = Ops.Defuzz(domains.CartForces, aggregated_conclusions)
    except:
        fuzzy_response = 0
    # KONIEC algorytmu regulacji
    #########################

    # Jeżeli użytkownik chce przesunąć wózek, to jego polecenie ma wyższy priorytet
    if control.UserForce is not None:
        applied_force = control.UserForce
        control.UserForce = None
    else:
        applied_force = fuzzy_response

    # Wyświetl stan środowiska oraz wartość odpowiedzi regulatora na ten stan.
    print(
        f"cpos={desired_position-cart_position:8.4f}, cvel={cart_velocity:8.4f}, pang={pole_angle:8.4f}, tvel={tip_velocity:8.4f}, force={applied_force:8.4f}")

    # Wykonaj krok symulacji
    env.step(applied_force)

    # Pokaż kotku co masz w środku
    env.render()

# Zostaw ten patyk!
env.close()

