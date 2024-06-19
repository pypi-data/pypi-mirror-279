#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finesse.virgo


# In[2]:


# create new Virgo instance
virgo = finesse.virgo.Virgo()

# create new Virgo, show everything is zero
virgo.print_dofs()
virgo.print_tunings()


# In[3]:


# change dofs by pretuning and show dofs and tunings change as expected
virgo.pretune()
virgo.print_dofs()
virgo.print_tunings()


# In[4]:


# zero the dofs and show the dofs are zero but the tunings remain
virgo.zero_dof_tunings()
virgo.print_dofs()
virgo.print_tunings()


# In[ ]:




