# nameko-management


**Notes**
-  The idea is for an easily customisable way to interact with a running nameko service, using an alternate access mechanism so as to not interfere or be blocked by the current running workers.
-  This would allow us to run health-checks, retrieve runtime-stats, examine what's workers are running right now etc.
Perhaps also in future it could allow us to kill stuck processes or tweak config values.
-  In this example version, the plugins are really the managment “entrypoints”. They have access to the container and can be invoked via a http call, so they define each function you can perform.
-  You can add your own plugin by creating a class and decorating with `@register_plugin` (or subclass the existing ones to modify the behaviour)
-  The given plugins just iterate over all dependencies calling methods that you may (or may not) have implemented.
-  And the new dependencies provided are there to return extra data to these plugins.
-  There’s a convenience `ManagementServiceMixin` that can be used, although the minimum requirement is to just have the Management dependency added to your service.
