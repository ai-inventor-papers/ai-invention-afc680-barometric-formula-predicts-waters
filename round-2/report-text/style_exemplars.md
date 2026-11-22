Register of these papers: medium-to-long sentences with frequent short sentences for emphasis, first person plural ("we") throughout, hedging limited to where the evidence is thin ("reasonably well", "could have"), numbers stated plainly with units, and dense citation brackets in introductions and results.

## Exemplar 1: A Deep Potential model for liquid-vapor equilibrium and cavitation rates of water (2023)

URL: https://arxiv.org/abs/2301.12008

### Abstract (verbatim text; markup normalised, e.g. plus-minus written as +/-)

Computational studies of liquid water and its phase transition into vapor have traditionally been performed using classical water models. Here we utilize the Deep Potential methodology -- a machine learning approach -- to study this ubiquitous phase transition, starting from the phase diagram in the liquid-vapor coexistence regime. The machine learning model is trained on ab initio energies and forces based on the SCAN density functional which has been previously shown to reproduce solid phases and other properties of water. Here, we compute the surface tension, saturation pressure and enthalpy of vaporization for a range of temperatures spanning from 300 to 600 K, and evaluate the Deep Potential model performance against experimental results and the semi-empirical TIP4P/2005 classical model. Moreover, by employing the seeding technique, we evaluate the free energy barrier and nucleation rate at negative pressures for the isotherm of 296.4 K. We find that the nucleation rates obtained from the Deep Potential model deviate from those computed for the TIP4P/2005 water model, due to an underestimation in the surface tension from the Deep Potential model. From analysis of the seeding simulations, we also evaluate the Tolman length for the Deep Potential water model, which is (0.091 +/- 0.008) nm at 296.4 K. Lastly, we identify that water molecules display a preferential orientation in the liquid-vapor interface, in which H atoms tend to point towards the vapor phase to maximize the enthalpic gain of interfacial molecules. We find that this behaviour is more pronounced for planar interfaces than for the curved interfaces in bubbles. This work represents the first application of Deep Potential models to the study of liquid-vapor coexistence and water cavitation.

### Introduction, third paragraph (verbatim text; markup normalised, e.g. plus-minus written as +/-)

Making use of the machinery provided by ML ab initio based models, here we study the liquid-vapor coexistence of water by means of Molecular Dynamics (MD) simulations. The liquid-vapor properties of water are well known from experiments [47]. From the computational side, the TIP4P/2005 non-polarizable rigid water model [10] has been highly successful at describing the liquid-vapor coexistence properties, reproducing the experimental phase diagram [48] and surface tension [49, 50, 51] reasonably well, as well as transport properties [48, 10, 52]. The TIP4P/2005 model has also been extensively benchmarked in the study of liquid-to-vapor and vapor-to-liquid phase transitions [53, 54, 55, 56, 57, 58, 59]. Therefore, we compare the Deep Potential Molecular Dynamics (DPMD) water model performance with that of TIP4P/2005 in addition to experimental data, when available.

### Conclusions, first paragraph (verbatim text; markup normalised, e.g. plus-minus written as +/-)

In this work, we explored the liquid-vapor phase behavior of a Deep Potential model based on ab initio energies and forces. This model was derived from the SCAN approximation of density functional theory [42]. The model has been shown to reproduce the phase diagram for the different ice phases [42] and to have a liquid-liquid phase transition in the supercooled regime [117]. We computed the phase diagram via DC simulations, and adjusted our vapor equilibrium densities to the experimental values, resulting in a shift of 40 K in the DPMD model. Once the model was tested and shifted, we compare its equilibrium properties with experimental data and the TIP4P/2005 model [10], one of the most benchmarked classical models for water [53, 141, 48, 49]. The surface tension of the DPMD model is lower than the one obtained from TIP4P/2005 and experiments. Nonetheless, by construction the DPMD model provides accurate results for other properties such as the vapor saturation pressure for a wide range of temperatures, between 300 and 600 K (Figure 2). Overall, once the temperature is shifted, the model reproduces most of the properties of liquid-vapor equilibrium, despite not having this regime included in its training. This result is especially remarkable since this is the first Deep Potential-based model to provide liquid-vapor properties in a computationally affordable time, with the primary drawback being the ~20% deviation in the surface tension.

### Conclusions, second paragraph (verbatim text, limitations and calibration; markup normalised)

Moreover, we study bubble nucleation in the cavitation regime. We make use of the NVT seeding method, a rare event technique already shown to be successful in determining the nucleation free energy barrier and the nucleation rate for simpler systems [85, 107] in cavitation events. We first performed NVT seeding calculations at 296.4 K, a temperature at which previous data from Umbrella Sampling are available for the TIP4P/2005 model and we confirm that the seeding technique provides consistent results with those from Menzl et al. [53]. The DPMD water model provides higher nucleation rates than the TIP4P/2005 model under the same stretching conditions. We show that this quantitative difference can be explained by the difference in surface tension between models, which persists for curved interfaces (Figure 4). Our results highlight once more the relevance of the surface tension and its change with curvature to critically control nucleation events [131, 53]. We could have obtained closer agreement between the TIP4P/2005 nucleation rates with those from the DPMD model if we did not apply the temperature shift, nonetheless we prioritised adjusting the model to obtain better equilibrium densities, in line with prior studies of water properties using the SCAN-derived DPMD model [116, 117, 118].

### Section outline

- I Introduction
- II Methods
  - II.1 DPMD Model
  - II.2 Simulation details
  - II.3 Seeding and Classical Nucleation Theory
- III Results and discussion
  - III.1 Vapor-liquid equilibrium in the DPMD model
  - III.2 Bubble nucleation
  - III.3 Determination of the Tolman length
  - III.4 Liquid-vapor interfacial characterization
- IV Conclusions
- Acknowledgments

Method organised by pipeline stage (model, simulation, then seeding analysis). Results organised by research question (equilibrium properties, nucleation, Tolman length, interface structure).

## Exemplar 2: Effects of gravity induced pressure variations for thermal liquid-gas phase-change simulations with the pseudopotential lattice Boltzmann method (2023)

URL: https://arxiv.org/abs/2301.12869

### Abstract (verbatim text; markup normalised, e.g. plus-minus written as +/-)

Direct simulations of phase-change and phase-ordering phenomena are becoming more common. Recently qualitative simulations of boiling phenomena have been undertaken by a large number of research groups. One seldom discussed limitations is that large values of gravitational forcing are required to simulate the detachment and rising of bubbles formed at a bottom surface. The forces are typically so large that neglecting the effects of varying pressure in the system becomes questionable. In this paper we examine the effect of large pressure variations induced by gravity using pseudopotential lattice Boltzmann simulations. These pressure variations lead to height dependent conditions for phase co-existence and nucleation of either gas or liquid domains. Because these effects have not previously been studied in the context of these simulation methods we focus here on the phase-stability in a one dimensional system, rather than the additional complexity of bubble or droplet dynamics. Even in this simple case we find that the different forms of gravitational forces employed in the literature lead to qualitatively different phenomena, leading to the conclusion that the effects of gravity induced pressure variations on phase-change phenomena should be very carefully considered when trying to advance boiling and cavitation as well as liquefaction simulations to become quantitative tools.

### Section outline (partial, from the full text)

- I. Introduction
- II. The pseudopotential LB method for non-ideal fluids
- III. Numerical investigation and theoretical analyses
  - A. Boiling on a flat surface with mixed wettability
    - 1. Numerical simulation
    - 2. Theoretical analysis and discussion
  - B. Boiling on a structured surface with homogeneous wettability
- IV. Summary

Method organised by component (method, then the two surface cases). Results organised by dataset or condition (flat surface, structured surface), with analysis following the simulation within each.

## Exemplar 3: How does boiling occur in lattice Boltzmann simulations? (2020)

URL: https://arxiv.org/abs/2005.07326

### Abstract (verbatim text; markup normalised, e.g. plus-minus written as +/-)

In recent years, the lattice Boltzmann (LB) method has been widely employed to simulate boiling phenomena. However, a very important issue still remains open, i.e., how does boiling occur in the LB simulations? For instance, the existing LB studies showed that the boiling on a hydrophobic surface begins at a lower wall superheat than that on a hydrophilic surface, which qualitatively agrees well with experimental studies, but no one has yet explained how this phenomenon appears in the LB simulations and what happened in the simulations after changing the wettability of the heating surface. In this paper, the LB boiling mechanism is revealed by analyzing boiling on a flat surface with mixed wettability and boiling on a structured surface with homogeneous wettability. Through a theoretical analysis, we demonstrate that, when the same wall superheat is applied, in the LB boiling simulations the fluid density near the heating surface decreases faster on a hydrophobic surface than that on a hydrophilic surface. Accordingly, a lower wall superheat can induce the phase transition from liquid to vapor on a hydrophobic surface than that on a hydrophilic surface. Furthermore, a similar theoretical analysis shows that the fluid density decreases fastest at concave corners in the case of a structured surface with homogeneous wettability, which explains why vapor bubbles are nucleated at concave corners in the LB simulations of boiling on structured surfaces.

### Section outline

The full text of this paper was not retrieved; its section headings are the same as those listed for Exemplar 2 (same authors' method family), so they are not repeated here.

## Style line (summary of the three papers above)

These papers use sentences of mixed length, with long sentences for the physics and short ones to close a paragraph. They write in the first person plural, rarely hedge outside the limitations, state numbers with units, and cite densely in introductions and results.
