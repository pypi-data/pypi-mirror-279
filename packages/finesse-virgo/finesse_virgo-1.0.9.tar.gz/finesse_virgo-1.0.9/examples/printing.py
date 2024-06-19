#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finesse.virgo


# # Printing Examples
# 
# 1. Print settings
# 2. Print lengths and frequencies
# 3. Print powers
# 4. Print DOFs
# 5. Print locks
# 6. Print tunings
# 7. Print thermal values

# In[2]:


# create a tuned Virgo model to use for this notebook.
virgo = finesse.virgo.Virgo()
virgo.make()


# ## 1. Print Model Settings

# In[3]:


virgo.print_settings()


# ## 2. Print Lengths and Frequencies

# In[4]:


virgo.print_lengths()


# ## 3. Print Carrier Powers

# In[5]:


virgo.print_powers()


# ## 4. Print DOF Values

# In[6]:


virgo.print_dofs()


# ## 5. Print Locks

# In[7]:


virgo.print_locks()


# ## 6. Print Tunings

# In[8]:


virgo.print_tunings()


# ## 7. Print Thermal Values

# In[9]:


virgo.print_thermal_values()

