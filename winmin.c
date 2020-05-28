#include <gtk/gtk.h>
#include <spice-client-gtk-3.0/spice-client-gtk.h>
#include <stdio.h>
SpiceMainChannel * mainchannel;
GtkWidget *window;
char** name;
char** sock;
int id;

gboolean resize_done (gpointer data)
{
  guint *gid = data;
  *gid = 0;
  resize(window);
  return FALSE;
}


gboolean on_configure_event (GtkWidget *window, GdkEvent *event, gpointer data)
{
  static guint gid = 0;
  if (gid)
    g_source_remove (gid);
  gid = g_timeout_add (250, resize_done, &gid);
  return FALSE;
}

void resize(GtkWidget * window) {
  printf("Resize!\n");
  int width, height;
  gtk_window_get_size(window, &width, &height);
  spice_main_channel_update_display(mainchannel, id, 0, 0, width, height, TRUE);
  spice_main_update_display_enabled(mainchannel,id,TRUE,TRUE);
  spice_main_send_monitor_config(mainchannel);
}

static void
activate (GtkApplication* app,
          gpointer        user_data)
{
  
  window = gtk_application_window_new (app);

  SpiceSession * session = spice_session_new();
  g_object_set(session,"uri",sock);
     //"spice+unix:///var/lib/libvirt/qemu/domain-1-winmin-base/spice.sock");
     //0.0.0.0:5900");

  SpiceChannel * channel =  spice_channel_new(session,1,id); // SPICE_CHANNEL(session);
  if (SPICE_IS_CHANNEL(channel)) {
    printf("Is spice channel\n");
  }
  else {
    printf("Not spice channel\n");
    exit(1);
  }

  printf("ID: %d\n",id);

  spice_session_connect(session);
  mainchannel =  SPICE_MAIN_CHANNEL(channel);
  if (SPICE_IS_MAIN_CHANNEL(mainchannel)) {
    printf("Good\n");
  }
  else {
    printf("Bad\n");
  }

  SpiceDisplay * display = spice_display_new(session,0);
  

  GtkWidget * displaywidget = GTK_WIDGET(display);
  gtk_container_add(GTK_CONTAINER(window),displaywidget);
    
  gtk_window_set_title (GTK_WINDOW(window), name);
  gtk_window_set_default_size (GTK_WINDOW (window), 900, 800);
  gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
  gtk_widget_show_all (window);

  resize(window);
  g_signal_connect(G_OBJECT(window), "configure-event",
        G_CALLBACK(on_configure_event), NULL);
}

int
main (int    argc,
      char **argv)
{
  GtkApplication *app;
  int status;
  name = argv[1];
  sock = argv[2];
  id = 0; //(int)strtol(argv[3], NULL, 10);
  app = gtk_application_new(NULL, G_APPLICATION_FLAGS_NONE); //"org.vlinkz.winmin"
  g_signal_connect (app, "activate", G_CALLBACK (activate), NULL);
  status = g_application_run (G_APPLICATION (app), NULL, NULL);
  g_object_unref (app);

  return status;
}
