ads = {
	'food': '토레타 광고',
	'fashion':  '블랙 ABC데이, 신발 광고',
	'car': 'Anuncio Volkswagen Arteon 2019 광고',
	'electronic': '갤럭시 S9 광고',
	'finance': '이베스트 투자증권 광고',
	'cosmetic': 'VANAV 광고',
	'home supplies': 'LG 프리빗 가전 광고',
	'game': '로스트아크 광고',
	'app': '야놀자 광고',
	'education': '파고다 토익 광고'
}
$(function() {
	var idx = 0;
	var lines;
	$.get('../playList.txt',function(data){
		lines = data.split('\n');
		lines.pop();
		$('video')[0].src = `ad/` + lines[idx++];
		var imgIndex=1;
		for(var e of lines){
			var name = e.split('.')[0]
			var path = name + '.jpg';
			var img = document.createElement('img');
			img.src = 'ad/' + path;
			$('.list-container > ul').append('<li>')
			$('.list-container > ul > li').last().append(img).append(`<p>${'time slot : ' + imgIndex.toString()}</p>`+`<p>${'category : ' + name }</p>` + `<p>${'ads contents : ' + ads[name]}`);
			imgIndex++;
		}
		$('video')[0].play();
	});
	$('video').bind('ended',function(){
		if(idx == lines.length-1) return;
		this.src = `ad//` + lines[idx++];
		this.play();
	});
});
