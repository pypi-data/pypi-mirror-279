#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finesse.virgo


# ## Optimize thermal lenses' focal length

# In[2]:


virgo = finesse.virgo.Virgo()

print('Before tuning')
# step 1: adjust the cavity lengths
virgo.adjust_PRC_length()
virgo.adjust_SRC_length()

# step 2: pretune
virgo.print_thermal_values()
virgo.optimize_TL(verbose=True)

virgo.plot_DARM()
virgo.print_thermal_values()


# In[ ]:




