#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finesse.virgo


# In[2]:


virgo = finesse.virgo.Virgo()


# # Tunings
# 
# Finesse 3 uses two values to determine the relative position of a mirror; the phi parameter and the relevant degrees of freedom.
# 
# We define a "phi tuning" as the phi parameter $\phi_{optic}$ (e.g., `NE.phi`) and a "dof tuning" as the DC value of the DOF $D_{dof}$ (e.g., `DARM.DC`).
# 
# We can then define the "tuning" of an optic as the sum of the phi tuning and the contribution from each DOF.
# 
# $ T_{i} = \phi_{i} + A_{ij} D^{j} $
# 
# This notebook covers the following:
# 
# 1) Print tunings
# 2) Get tunings
# 3) Set tunings
# 4) Zero dof tunings

# ## 1) Print tunings
# 
# The tunings can be displayed in a summary table using `print_tunings()`. The tunings will be shown in both degrees and picometers in addition to the phi and dof tunings in degrees.

# In[3]:


virgo.print_tunings()


# ## 2) Return the current tunings
# 
# The current tunings can be returned using `get_tunings()`. This will return a dictionary keyed by optic.
# 
# Similarly, the current phi or dof tunings can be returned using `get_phi_tunings()` or `get_dof_tunings()`.

# In[4]:


# get all the tunings (phi+DOF)
print('Tunings', virgo.get_tunings())

# get the phi or dof tunings
print('Phi tunings', virgo.get_phi_tunings())
print('DOF tunings', virgo.get_dof_tunings())

print(virgo.get_tuning('NE'))


# ## 3) Set tunings
# 
# The tunings can be set by passing a dictionary to `set_tunings()`. The tunings will be applied directory to the mirrors as phi tunings and the dof tunings will be reset.

# In[5]:


virgo.set_tunings({
    "NE": 1,
    "WE": 1,
    "NI": 1,
    "WI": 1,
    "PR": 1,
    "SR": 1,
})

virgo.print_tunings()


# Phi and DOF tunings can also be set separately.

# In[6]:


virgo.set_phi_tunings({
    "NE": 1,
    "WE": 1,
    "NI": 1,
    "WI": 1,
    "PR": 1,
    "SR": 1,
})

virgo.set_dof_tunings({
    "DARM": 1,
    "CARM": 1,
    "MICH": 1,
    "PRCL": 1,
    "SRCL": 1,
})

virgo.print_tunings()


# ## 4) Zeroing DOF tunings
# 
# It may be intuitive to store all tuning information in the mirrors' phi tunings. This can be done with `zero_dof_tuning()` which will relocate the DOF tunings into the phi tunings.

# In[7]:


virgo.zero_dof_tunings()

virgo.print_tunings()

