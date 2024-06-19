from CompNeuroPy import (
    CompNeuroExp,
    CompNeuroMonitors,
    CompNeuroModel,
    current_step,
    current_ramp,
    PlotRecordings,
)
from CompNeuroPy.full_models import HHmodelBischop
from ANNarchy import dt, setup, get_population
import matplotlib.pyplot as plt
import numpy as np

setup(dt=0.01)


class MyExp(CompNeuroExp):

    def run(self, model: CompNeuroModel, E_L: float):
        # PREPARE RUN
        self.reset()
        self.monitors.start()
        # SET E_L PARAMETER
        get_population(model.populations[0]).E_L = E_L
        # SIMULATION
        ret_current_ramp = current_ramp(
            pop=model.populations[0], a0=0, a1=100, dur=1000, n=50
        )
        self.reset(parameters=False)
        ret_current_step = current_step(
            pop=model.populations[0], t1=500, t2=500, a1=0, a2=50
        )
        # OPTIONAL DATA OF RUN
        self.data["population_name"] = model.populations[0]
        self.data["time_step"] = dt()
        self.data["current_arr"] = np.concatenate(
            [ret_current_ramp["current_arr"], ret_current_step["current_arr"]]
        )
        # RETURN RESULTS
        return self.results()


# The model is a single population (consisting of 1 neuron) of a Hodgkin & Huxley neuron.
model = HHmodelBischop()
model.populations

# Create the experiment, recording the membrane potential of the models first population.
my_exp = MyExp(monitors=CompNeuroMonitors({model.populations[0]: ["v"]}))

# Set the membrane potential of the model for the initial state during the experiment to -90 mV.
print(f"Compilation state v = {get_population(model.populations[0]).v}")
get_population(model.populations[0]).v = -90.0
print(f"Changed state v = {get_population(model.populations[0]).v}")
my_exp.store_model_state(compartment_list=model.populations)

# Run the experiment twice with different leakage potentials
results_run1: CompNeuroExp._ResultsCl = my_exp.run(model=model, E_L=-68.0)
results_run2: CompNeuroExp._ResultsCl = my_exp.run(model=model, E_L=-90.0)

# PlotRecordings allows to easily get overview plots of the recordings of a single recording chunk.
for chunk in range(2):
    PlotRecordings(
        figname=f"example_experiment_chunk_{chunk}.png",
        recordings=results_run1.recordings,
        recording_times=results_run1.recording_times,
        chunk=chunk,
        shape=(1, 1),
        plan={
            "position": [1],
            "compartment": [results_run1.data["population_name"]],
            "variable": ["v"],
            "format": ["line"],
        },
    )

# Each experiment run created 2 recording chunks. They all start at time 0 (because of resetting the model, see above). The function combine_chunks() can be used to combine the chunks into a single recording time and value array.
time_arr1, data_arr1 = results_run1.recording_times.combine_chunks(
    recordings=results_run1.recordings,
    recording_data_str=f"{results_run1.data['population_name']};v",
    mode="consecutive",
)
time_arr2, data_arr2 = results_run2.recording_times.combine_chunks(
    recordings=results_run2.recordings,
    recording_data_str=f"{results_run2.data['population_name']};v",
    mode="consecutive",
)
current_arr = results_run1.data["current_arr"]

# create a plot of the combined recordings
plt.figure()
plt.subplot(211)
plt.plot(time_arr1, data_arr1, label="E_L = -68.0")
plt.plot(time_arr2, data_arr2, label="E_L = -90.0")
plt.plot(
    [time_arr1[0], time_arr1[-1]], [-90, -90], ls="dotted", label="initial v = -90.0"
)
plt.legend()
plt.ylabel("Membrane potential [mV]")
plt.subplot(212)
plt.plot(time_arr1, current_arr, "k--")
plt.ylabel("Input current")
plt.xlabel("Time [ms]")
plt.tight_layout()
plt.savefig("example_experiment_combined.png")
