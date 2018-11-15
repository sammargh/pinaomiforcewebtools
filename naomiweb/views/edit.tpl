% include('header.tpl', title='Edit')

<div class="container">
	% include('navbar.tpl', activePage='edit')

	% if defined('did_edit'):
	<div class="alert alert-success"><span class="glyphicon glyphicon-ok"></span> Saved changes!</div>
	%end

	<form class="form-horizontal" action="{{hashid}}" method="POST" role="form">
		<input type="hidden" name="filename" value="{{filename}}">
		<h2></h2>
		<div class="row container">
			<div class="form-group">

				<label class="col-sm-2 control-label">{{filename}}</label>
				<div class="col-sm-3">
					<select class="form-control" id="games" name="games">
					% for g in games_list:
						<option value="{{g[0]}}" {{"selected" if game_title == g[1] else ""}}>{{g[1]}}</option>
					% end
					</select>
				</div>
			</div>
		</div>
		
		<div class="row container">
			<div class="col-md-2">
				<button type="submit" class="btn btn-default">Save</button>
			</div>
		</div>
	</form>
</div>

% include('footer.tpl')
