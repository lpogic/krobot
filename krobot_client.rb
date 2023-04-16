require 'mqtt'

class HR8825
  def initialize dir_pin, step_pin, enable_pin
    @dir_pin = dir_pin
    @step_pin = step_pin
    @enable_pin = enable_pin
  end

  def rotate dir, speed = 600
    MQTT::Client.connect('localhost', 5678) do |c|
      if dir == :back
        c.publish("gpio", "high/#{@dir_pin}")
      else
        c.publish("gpio", "low/#{@dir_pin}")
      end
      c.publish("gpio", "pwm/50/#{speed}/#{@step_pin}")
      c.publish("gpio", "high/#{@enable_pin}")
    end
  end


  def stop
    MQTT::Client.connect('localhost', 5678) do |c|
      c.publish("gpio", "low/#{@enable_pin}")
      c.publish("gpio", "pwm/0/100/#{@step_pin}")
    end
  end
end

motor1 = HR8825.new 13, 19, 12
motor2 = HR8825.new 24, 18, 4
  
begin
  MQTT::Client.connect('localhost', 5678) do |c|
    #c.subscribe '#'
    c.get('krobot') do |topic,message|
      puts message
      case message
      when "stop"
        motor1.stop
        motor2.stop
      when "front_slow"
        motor1.rotate :front, 300
        motor2.rotate :front, 300
      when "front"
        motor1.rotate :front
        motor2.rotate :front
      when "front_fast"
        motor1.rotate :front, 900
        motor2.rotate :front, 900
      when "back_slow"
        motor1.rotate :back, 300
        motor2.rotate :back, 300
      when "back"
        motor1.rotate :back
        motor2.rotate :back
      when "back_fast"
        motor1.rotate :back, 900
        motor2.rotate :back, 900
      when "left"
        motor1.rotate :front
        motor2.rotate :back
      when "right"
        motor1.rotate :back
        motor2.rotate :front
      end
    end
  end
rescue Interrupt
  puts " Bye Bye!"
end
