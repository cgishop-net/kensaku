#!/usr/bin/perl


#┌─────────────────────────────────
#│  kensaku v1.00 (2012/05/27)
#│  Copyright (c) Dotmatrix
#│  info@cgishop.net
#│  http://cgishop.net/
#└─────────────────────────────────
$ver = 'kensaku v1.00';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対しても作者は一切の責任を負いません。
#│ 2. 設置に関する質問、サポートは行いません。
#│    直接メールによる質問は一切お受けしておりません。
#│ 3. ご理解ご協力のほど、よろしくお願いいたします。
#└─────────────────────────────────
#
# 【ファイル構成例】
#
#  public_html (ホームディレクトリ)
#      |
#      +-- kensaku / kensaku.cgi  [755]ソフト本体






#=== 受信処理=== ==================================================


if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

#=== デコード処理 =================================================


@pairs = split(/&/,$buffer);

foreach $pair (@pairs) {

	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	
	
	$FORM{$name} = $value;
}

# コメント本文の改行処理
	$FORM{'keywd'} =~ s/\r\n/<br>/g;
	$FORM{'keywd'} =~ s/\r/<br>/g;
	$FORM{'keywd'} =~ s/\n/<br>/g;



$ab = $FORM{'keywd'};
$ab =~ s/<br>//g;
$num = length("$ab");

#=======================================================================


#既存ファイルを読み込み、配列@aaa に入れる
open (IN,"address.csv");
@aaa = <IN>;
close (IN);

#=======================================================================

#ヘッダを出力する
print "Content-type: text/html\n\n";
print "<META http-equiv=\"Content-Type\" content=\"text/html; charset=utf8\">";

if ($FORM{'keywd'} eq "") #検索キーワードが空の場合のメッセージ
{
	print "<HR><FONT color=red>検索キーワードが入力されていません</FONT><HR>";
}
else #検索キーワードが有る場合の上部メッセージ
{
	print "<HR><FONT color=red>$FORM{'keywd'}</FONT> で検索した結果<HR>";
}

$count = 0; #ヒット件数カウント用の変数を初期化する
foreach $youso (@aaa)
{
	if ($youso =~ /$FORM{'keywd'}/i) #マッチしたら以下の処理を実行
	{
		($view1,$view2,$view3,$view4,$view5,$view6,$view7) = split (/,/,$youso);
		print "<BR><BR><B>No.</B> $view1<BR>";
		print "<B>名前：</B> $view2<BR>";
		print "<B>住所：</B> $view3<BR>";
		print "<B>電話番号：</B> $view4<BR>";
		print "<B>携帯電話番号：</B>  $view5<BR>";
		print "<B>備考：</B><BR>$view6";
		
		$count++;
	}
}

if ($count == 0) #カウンタが 0の場合はマッチしなかった為、メッセージ出力する
{
	print "キーワードにマッチするデータはありませんでした。";
	print "<BR><A href=\"index.htm\">戻る</A><BR>";
}
else #それ以外はマッチしているので、件数を表示する
{	
	print "<BR><BR><BR><HR>$count件のデータがマッチしました。<HR>";
	print "<BR><A href=\"index.htm\">戻る</A><BR>";
}

exit;
