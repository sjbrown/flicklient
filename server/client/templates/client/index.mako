<table>
<tbody>
<tr>
<td>
    <h1><a href="/client/?startover=1">Flicklient!</a></h1>
</td>
<td>
    <ul>
        % if user.is_authenticated():
            <li>You are user ${ user }</li>
            <li><a href="/client/log_out">Log out</a></li>
            <li><a href="/client/show_faves">See my favourites</a></li>
        % else:
            <li><a href="/client/sign_up">Sign up</a></li>
            <li><a href="/client/log_in">Log in</a></li>
        % endif
    </ul>
</td>
</tr>
</tbody>
</table>

% for message in messages:
    <span style="color:red">${ message }</span>
% endfor

<table border="1">
<tbody>

% for photo in photos[:20]:

    <tr>
    <td>
    % if user.is_authenticated():

        % if photo.metadata['link'] in faves:
            <b>:)</b>
            <form method="post" action="/client/unfavourite">
                ${ csrf }
                <input type="hidden"
                       name="link" value="${ photo.metadata['link'] }" />
                <input type="submit" value="Unfavourite" />
            </form>
        % else:
            <form method="post" action="/client/favourite">
                ${ csrf }
                <input type="hidden"
                       name="link" value="${ photo.metadata['link'] }" />
                <input type="submit" value="Favourite" />
            </form>
        % endif

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

% if not at_the_end:
    <a href="?next=1">Next ...</a>
% else:
    Click the Flicklient title to start over
% endif
