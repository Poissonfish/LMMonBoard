from ..lib import *

def page_about():
    text = Div(text="""
    <h1> About </h1>
    <h2> Authors </h2>
    Chunpeng James Chen: niche@ucdavis.edu <br>
    Hao Cheng: qtlcheng@ucdavis.edu

    <h2> Examples </h2>
    Example datasets in this app are collected from the book
    "Mrode,R.A. (2013) Linear models for the prediction of animal breeding values 3rd ed. CABI, Boston, MA".

    <h3> Animal Model (Chapter 3.3) </h3>

    It's a dataset for modeling the pre-weaning gain (WWG, kg) in beef calves.
    The dataset contains the information of animals and their ancestors (sire and dam),
    it also contains phenotypes (WWG) and the sexes of each animals. The animal model is defined as:
    <br><center>
    y<sub>ij</sub> = p<sub>i</sub> + a<sub>j</sub> + e<sub>ij</sub>
    </center><br>
    Where the ith sex is a fixed effect and is denoted as pi;
    aj is the jth animal effect (random);
    And eij stands for the residual of the jth animal of the ith sex.

    <h3> Repeatability Model (Chapter 4.2) </h3>

    Fat yields (kg) are recorded for 5 dairy cows, 
    and each cow has two records for the 1st and the 2nd parity. 
    Different herd-year-season (HYS) effects are considered in the dataset as well, 
    and both HYS and parities are fitted as fixed effects in this example. 
    Below is the equation of the model:
    <br><center>
    y = X<sub>b</sub> + Z<sub>a</sub> + W<sub>pe</sub> + e
    </center><br>
    where X, Z, and W are incidence matrixs of fixed, animal, 
    and permanent envirnomental effects, respectively. 
    y is fat yield; b is the fixed effects; a is additive animal effect; 
    pe is non-additive animal effects; and e is a vector of random residual effect. 

    <h3> Common Environmental Effects (Chapter 4.3) </h3>

    Ten offspring piglets from three dams are recorded for their weaning weight (kg). 
    This model is designed to estimate sex effects and predict animal effects (piglet) 
    and environment effects contributed from their dams. The model is described as:  
    <br><center>
    y = X<sub>b</sub> + Z<sub>a</sub> + W<sub>c</sub> + e
    </center><br>
    where X, Z, and W are incidence matrixs of fixed, animal, 
    and common envirnomental effects, respectively. 
    y is fat yield; b is the fixed effects; a is additive animal effect; 
    c is common environmentral effects (dams); and e is a vector of random residual effect. 

    <h3> Maternal Model (Chapter 7.2) </h3>

    The data records the birth weight (kg) for a group of beef calves. 
    This model aims to estimate fixed effects of pen and herds, 
    it also predict the animal and maternal effects structured by the pedigree. 
    In addition, maternal effects can be further fitted as permanent envirnomental 
    effects as offsprings are affected by milk produced from their dams. 
    The model can be wrritten as: 
    <br><center>
    y = X<sub>b</sub> + Z<sub>u</sub> + W<sub>m</sub> + S<sub>pe</sub> + e
    </center><br>
    where X, Z, W, and S are incidence matrixs of fixed, animal, maternal, 
    and permanent envirnomental effects, respectively. 
    b = the effects of pan and herbs; u = animal random effects; 
    m = maternal random effects; pe = permanent environmental effects; 
    and e = a vector of residuals.

    """, width=1000, style={'font-size': '200%'})

    return column(text)


# <h1 > LMMonBoard < /h1 >
# <h2 > header 2 < /h2 >
# abstjkljioej lj
# salkdjf ij
# alskdj
# <ul >
# <li>Coffee</li>
# <li>Tea</li>
# <li>Milk</li>
# </ul>
