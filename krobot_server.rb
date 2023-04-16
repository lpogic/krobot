require 'sinatra'
require 'mqtt'

set :bind, '0.0.0.0'

template = <<~HTML
  <style>
    button {
      font-size: 15vh;
    }
  </style>
  <form method="POST" style="width: 100%; height: 100%; display: grid; grid-template-columns: auto auto auto; grid-template-rows: auto auto auto; gap: 0.1em">
    <button name="control" value="front_slow">&UpArrow;</button>
    <button name="control" value="front">&DoubleUpArrow;</button>
    <button name="control" value="front_fast">&#x290A;</button>
    <button name="control" value="left">&circlearrowleft;</button>
    <button name="control" value="stop">STOP</button>
    <button name="control" value="right">&circlearrowright;</button>
    <button name="control" value="back_slow">&DownArrow;</button>
    <button name="control" value="back">&DoubleDownArrow;</button>
    <button name="control" value="back_fast">&#x290B;</button>
  </form>
HTML

get '/do' do
  template
end

post '/do' do
  control = params['control']

  MQTT::Client.connect('localhost', 5678) do |c|
    c.publish 'krobot', control
  end
  template
end
