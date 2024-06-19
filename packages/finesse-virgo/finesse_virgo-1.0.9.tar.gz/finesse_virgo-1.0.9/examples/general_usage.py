#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finesse.virgo
import finesse.analysis.actions as fa
from finesse.virgo.actions import DARM_RF_to_DC


# In[2]:


# simple make, can be configured, returns Finesse model
model = finesse.virgo.make_virgo(
    maxtem="off",
    thermal_state="design-matched",
    use_3f_error_signals=False,
    with_apertures=False,
    x_scale=1,
    zero_k00=False,
    display_plots=False,
    verbose=False,
)


# In[3]:


# can also make from a modified model
virgo = finesse.virgo.Virgo()
virgo.model.parse("var test 1")
virgo.make()
print('test =', virgo.model.test.value)


# In[4]:


# or make step by step
virgo = finesse.virgo.Virgo()
virgo.model.parse("var state 0")
# virgo.adjust_recycling_cavities()
virgo.adjust_recycling_cavity_length("PRC", "lPRC", "lPOP_BS")
virgo.adjust_recycling_cavity_length("SRC", "lSRC", "lsr")
virgo.pretune() # now in pretuned state

# and modify the model in between
virgo.model.state.value += 1

virgo.apply_dc_offset()
virgo.optimize_demodulation_phase()
virgo.model.run(fa.RunLocks(method="newton"))
virgo.model.state.value += 1

virgo.model.run(DARM_RF_to_DC()) # now in dc locked state
virgo.model.state.value += 1

print('state =', virgo.model.state.value)


# In[5]:


# the model is accessible and can be replaced, but this breaks state
#   meaning configurable settings are potentially wrong
#   and would need to be set manually
virgo = finesse.virgo.Virgo()
virgo.print_thermal_values()

virgo.model = finesse.virgo.make_virgo(thermal_state="cold")
virgo.print_thermal_values()

print(virgo.thermal_state) # should be "cold"
virgo.thermal_state = "cold"

virgo.model.parse("var test 1")
virgo.model.unparse()
virgo.model.mismatches_table()


# In[6]:


virgo = finesse.virgo.Virgo()
virgo.plot_QNLS()
virgo.make()
virgo.plot_QNLS()


# In[7]:


# can be more verbose and display plots
virgo = finesse.virgo.Virgo(verbose=True, display_plots=True)
virgo.make()


# In[8]:


# individual steps can also be made verbose
# TODO: can improve verbosity
virgo = finesse.virgo.Virgo()

# adjust the recycling cavity lengths
virgo.adjust_PRC_length()
virgo.adjust_SRC_length()

# pretune by maximizing cavity power and minimizing dark fringe
virgo.pretune(verbose=True) # now in pretuned state

# prepare to run the locks
virgo.optimize_demodulation_phase()
virgo.optimize_lock_gains()

# run the locks
virgo.model.run(fa.RunLocks(method="newton")) # now in rf locked state

# switch DARM to a DC lock with offset
virgo.model.run(DARM_RF_to_DC()) # now in dc locked state

virgo.plot_QNLS()


# In[9]:


# similar to a Finesse model, Virgo can also be deepcopied for branching purposes.
virgo1 = finesse.virgo.Virgo()
virgo1.model.parse('var test 0')

virgo2 = virgo1.deepcopy()
virgo2.model.test.value = 1

print('virgo1.test =', virgo1.model.get('test').value)
print('virgo2.test =', virgo2.model.get('test').value)


# In[ ]:




