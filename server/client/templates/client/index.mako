<h1>Flicklient!</h1>
<ul>
    % if user:
        <li>You are user ${ user }</li>
    % else:
        <li>Sign up</li>
    % endif
</ul>

<table border="1">
<tbody>
<tr>
<td>
<a>Favourite</a>
</td>
<td>
    <a href="${ metadata[0]['link'] }"
    ><img src="${pics[0]}"
          alt="${ metadata[0]['title']}"
          title="${ metadata[0]['title']}"
    /></a></td>
<td>
    <ul>
      <li>${ metadata[0]['link'] }
      <li>${ metadata[0]['title'] }
      <li>${ metadata[0]['description'] }
      <li>${ metadata[0]['author'] }
      <li>${ metadata[0]['date_taken'] }
      <li>${ metadata[0]['tags'] }
    </ul>
</td>
</tr>
</tbody>
</table>
