<h1>Flicklient!</h1>
<ul>
    % if user.is_authenticated():
        <li>You are user ${ user }</li>
        <li><a href="/client/log_out">Log out</a></li>
    % else:
        <li><a href="/client/sign_up">Sign up</a></li>
        <li><a href="/client/log_in">Log in</a></li>
    % endif
</ul>

<table border="1">
<tbody>

% for photo in photos[:20]:

    <tr>
    <td>
    % if user.is_authenticated():
        <a>Favourite</a>
    % else:
        <i>Log in to mark your favourites</i>
    % endif
    </td>
    <td>
        <a href="${ photo.metadata['link'] }"
        ><img src="${photo.media}"
              alt="${ photo.metadata['title']}"
              title="${ photo.metadata['title']}"
        /></a></td>
    <td>
        <ul>
          <li>${ photo.metadata['link'] }
          <li>${ photo.metadata['title'] }
          <li>${ photo.metadata['description'] }
          <li>${ photo.metadata['author'] }
          <li>${ photo.metadata['date_taken'] }
          <li>${ photo.metadata['tags'] }
        </ul>
    </td>
    </tr>

% endfor

</tbody>
</table>
