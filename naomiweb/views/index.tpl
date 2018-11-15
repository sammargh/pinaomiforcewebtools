% include('header.tpl', title='NetDIMM Loader')

<div class="container">
	% include('navbar.tpl', activePage='games')
  	
		<div class="row container" id="filters">
			Filters
			<select class="form-control filter-group" id="filter-group" name="filter-group">
			% for fg in filter_groups:
				<option value="{{fg[0]}}">{{fg[1]}}</option>
			% end
			</select>
			<select class="form-control filter-value" id="filter-value" name="filter-value">
				% for fg in filter_values:
					<optgroup id="{{fg[0]}}" label="select" class="hidden">
					% for g in fg[1]:
						<option value="{{g[0]}}">{{g[1]}}</option>
					% end
					</optgroup>
				% end
			</select>
		<button id="add-filter" class="btn btn-default">Add</button>

	</div>
	<div class="row container">
		Active Filters:
		% for f in activefilters:
			<span><a class="rm-filter" href="/filter/rm/{{f[0]}}/{{f[1]}}">{{f[0]}} = {{f[1]}}</a></span>
		% end
	</div>
	% if defined('games'):
	<h4>Choose a game to play</h4>
	% for game in games:
	<a class="edit-link" href="edit/{{game.checksum}}"><span class="glyphicon glyphicon-edit"></span></a>
		<div class="label label-default game {{game.status}}">
			<div class="col0">
				<img src="/static/images/{{game.id}}.jpg" alt="game image">
			</div>
			<div class="col1">
				<div><a class="game-link" href="load/{{game.checksum}}">{{game.name}}</a></div>
				<div><span class="filename"><em>{{game.filename}}</em></span> <span class="label label-default fileinfo">{{round(game.size/float(1024*1024), 1)}} MB</span></div>
			</div>
		</div>
		
	% end
	% end


	% if not defined('games'):
	<div class="alert alert-danger"><span class="glyphicon glyphicon-warning-sign"></span> No games were found! Verify that the directory set on the configuration screen exists and contains valid NAOMI games.</div>
	% end

</div>

% include('footer.tpl')
