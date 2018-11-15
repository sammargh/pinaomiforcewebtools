<nav class="navbar navbar-default" role="navigation">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/">NetDIMM Loader</a>
    </div>

    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li {{!'class="active"' if activePage=='games' else ''}}><a href="/">Games</a></li>
        <li {{!'class="active"' if activePage=='config' else ''}}><a href="/config">Configuration</a></li>
      </ul>
    </div>
  </div>
</nav>
