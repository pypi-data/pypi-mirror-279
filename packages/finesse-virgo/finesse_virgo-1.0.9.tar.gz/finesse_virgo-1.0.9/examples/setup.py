#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finesse.virgo

finesse.init_plotting()


# # Pretuning Notebook
# 
# This notebook can be used to view information on a Virgo model.
# 
# 0. Load the model
# 1. Lengths status
# 2. Pretune status
# 3. Plot pretuning powers
# 4. Display error signals
# 5. Plot error signals
# 6. Display sensing matrix
# 7. Plot sensing matrix radar plots

# ## 0. Load the model

# In[2]:


virgo = finesse.virgo.Virgo(verbose=True)


# ## 1. Lengths status

# In[3]:


virgo.adjust_PRC_length()
virgo.adjust_SRC_length()

virgo.print_lengths()


# ## 2. Pretune status

# In[4]:


virgo.pretune()
virgo.print_pretune_status()


# ## 3. Plot pretuning powers

# In[5]:


virgo.plot_powers();


# ## 4. Display error signals

# In[6]:


virgo.print_error_signals()


# ## 5. Plot error signals

# In[7]:


virgo.plot_error_signals();


# ## 6. Display sensing matrix

# In[8]:


virgo.print_sensing_matrix()


# ## 7. Plot sensing matrix radar plots

# In[9]:


virgo.plot_sensing_matrix();

