#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finesse.virgo

finesse.init_plotting()


# # Locks
# 
# 1) Creating Virgo without locks
# 2) Adding locks
# 3) Printing locks
# 4) Displaying error signals

# ## 1) Creating Virgo without locks
# 
# By default, the locks are added according to the control scheme. This can be skipped by using `add_locks=False` to add them later.

# In[2]:


virgo = finesse.virgo.Virgo(add_locks=False)


# ## 2) Adding locks
# 
# Locks are added according to the control scheme which can be modified manually before adding them by calling `add_locks()`.

# In[3]:


print(virgo.control_scheme)

virgo.add_locks()


# ## 3) Printing locks
# 
# You can use `print_locks()` to display the state of the locks.
# 
# It will display the lock parameters in addition to the accuracies in units of degrees, meters, and Watts and the optical gains in units of W/deg, W/rad, and W/m.

# In[4]:


# default usage
virgo.print_locks()


# Optionally, adjusted lock gains ($ factor * (-1/optical gain)$) can be displayed by providing a dictionary of gain adjustments. This may be needed to make the locks more robust for a particular set up.
# 
# Note: this is just a calculation without changing the locks. Any changes will need to be added manually.

# In[5]:


# with gain adjustments
virgo.print_locks(gain_adjustments={
    "DARM": 0.1, 
    "CARM": 0.9, 
    "PRCL": 0.9, 
    "MICH": 0.001, 
    "SRCL": 0.02,
})


# ## 4) Displaying Error Signals
# 
# The value of the error signals can be displayed with `print_error_signals()` and returned with `get_error_signals()`.

# In[6]:


# pretune and lock the ifo
virgo.make(dc_lock=False)

# display the error signal values
virgo.print_error_signals()

# return as a dictionary keyed by dof
virgo.get_error_signals()


# In[ ]:




