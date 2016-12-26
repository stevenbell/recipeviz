// From: http://bl.ocks.org/stevemandl/02febfc129131db79adf
// Author: Steven Mandl

updatingCrossfilter = function(cbk){
		var c = crossfilter(); //the underlying crossfilter
		//function to get a serial ID
		var _getID = (function(){var id = 0; return function(){ return id++;}})(),
			//allows the client to subscribe to update events
			_listener = d3.dispatch("update", "startUpdate");

		// registers an event handler
	    c.on = function (event, listener) {
	        _listener.on(event, listener);
	        return c;
	    };
	    
	    //the unique ids of the data elements of the crossfilter
		c._ids = d3.set();
		//the dimension to track the ids
		c._idDim = c.dimension(function(d) { return d._id; });
		//backup add and remove for later
		c._add = c.add;
		c._remove = c.remove;

		// add new data
		c.add = function(newData){
			newData.forEach(function(d){
				d._id = _getID();
				this._ids.add(d._id);}, this);
			return c._add(newData);
		};

		//remove data matching the current filter(s)
		c.remove = function(){
			this._idDim
				.top(Infinity)
				.forEach(function(d){this._ids.remove(d._id);}, this);
			return c._remove();
		};
		
		//update newData by replacing the elements with matching id's
		c.update = function(newData){
			_listener.startUpdate();
			c.liftFilters();
			newData.forEach(function(d){
				c._idDim.filter(d._id);
				c.remove();
			}, this);
			c._idDim.filterAll();
			c.add(newData);
			c.restoreFilters()
			_listener.update();
			return c;
		};

	    //temporarily lift filters from all charts' dimensions, saving them to for restoreFilters() later
		//TODO: listen for filter changes so this is not dependent on dc
	    c.liftFilters = function(){
	    	dc.chartRegistry.list().forEach(function(d){
	    		d._liftedFilters = d.filters();
	    		d.filterAll();
	    	});
	    	return c;
	    };

	    //restore filters to charts' dimensions previously saved by liftFilters()
	    c.restoreFilters = function(){
	    	dc.chartRegistry.list().forEach(function(d){
	    		if (d._liftedFilters){
	    			d._liftedFilters.map(d.filter);
		    		delete d._liftedFilters;
	    		}
	    	});
	    	return c;
	    };
	    
		//sanitize cbk as a function
		if (cbk && typeof arguments[0] != "function"){
			var o = cbk;
			cbk = function(c){return c.add(o);};
		}
		cbk && cbk(c);
		return c;
	}