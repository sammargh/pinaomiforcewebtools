$('.game').click(function(event)
{
	event.preventDefault();
	
	$.ajax
	({
		url: $(this).find('.game-link').attr('href'),
		type: 'get',
		success: function(result)
		{
			var json = $.parseJSON(result)
			$('#status').html(json.message);
		}
	});
});


//Filters
$('.filter-group').change(function() {
	var val_select = $('select[name=filter-value].filter-value');
	val_select.children().addClass("hidden");
	val_select.children('optgroup#' + $(this).val()).removeClass('hidden');
	
	val_select.val(val_select.children('optgroup:not(.hidden)').children('option:first').val());
});

$('#add-filter').click(function(event) {
	event.preventDefault();
	
	$.ajax
	({
		url: "/filter/add/" + $('#filter-group option:selected').text() + "/" + $('#filter-value option:selected').text(),
		type: 'get',
		success: function(result)
		{
			location.reload();
		}
	});
});

$('.rm-filter').click(function(event) {
	event.preventDefault();

	$.ajax
	({
		url: $(this).attr('href'),
		type: 'get',
		success: function(result)
		{
			location.reload();
		}
	});
});


//remove hidden class from first option group by efault
$('select[name=filter-value].filter-value').children('optgroup#1').removeClass('hidden')

$('#rescan-games').click(function(event) {
	event.preventDefault();

	$.ajax
	({
		url: "/rescan",
		type: 'get',
		success: function(result)
		{
			$(this).attr('disabled','disabled');
			//location.reload();
		}
	});
});

//Status bar

var source = new EventSource("/status");
source.onmessage = function(event) {
	var json = $.parseJSON(event.data);
	if (json.status != 0) {
		$('#status').addClass('error');
	} else
		$('#status').removeClass('error');
	$("#status").html(json.message);
};
