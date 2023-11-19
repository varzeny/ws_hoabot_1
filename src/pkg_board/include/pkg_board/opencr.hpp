#include <rclcpp/rclcpp.hpp>
#include <boost/asio.hpp>

#include <std_msgs/msg/string.hpp>


#define BAUDRATE_BOARD 115200


// 보드와 연결된 시리얼 포트를 읽고 알맞은 콜백을 발동시키며, 특정 노드를 구독 하는 보드제어 노드
class NodeBoard : public rclcpp::Node
{
    public:
    
        boost::asio::io_service io_service;
        boost::asio::serial_port serial;
        std::vector<int32_t> data_toBoard;


        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_board_cmd;



        NodeBoard();
        ~NodeBoard();

        void callback_board_cmd(const std_msgs::msg::String::SharedPtr msg);

        void toBoard(const std::vector<int32_t>& data);

};