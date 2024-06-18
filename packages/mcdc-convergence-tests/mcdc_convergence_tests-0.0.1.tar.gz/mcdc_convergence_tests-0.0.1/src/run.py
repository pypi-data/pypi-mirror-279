import main
import matplotlib.pyplot as plt
def test(particlenums,sourcetype,loud = True,createdata = True):
    main.runtest(particlenums,sourcetype,loud,createdata)
    plt.show(block = False)
    plt.pause(0.001) # Pause for interval seconds.
    input("hit[enter] to end.")
    plt.close('all') # all open plots are correctly closed after each run
    
