package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.Favor;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.vo.FavorVo;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 张小明
* @description 针对表【favor】的数据库操作Mapper
* @createDate 2024-06-25 14:11:43
* @Entity com.kclgroup.backend.pojo.entity.Favor
*/
@Mapper
public interface FavorMapper extends BaseMapper<Favor> {
    @Select("select * from favor where username=#{username} and favor_stock_code=#{stockCode}")
    Favor getFavor(String username, String stockCode);

    @Insert("insert into favor(username,favor_stock_code,create_time) values (#{username},#{stockCode},now())")
    void addFavor(String username,String stockCode);

    @Delete("delete from favor where username=#{username} and favor_stock_code=#{stockCode}")
    void deleteFavor(String username, String stockCode);
    @Select("select i.stock_name,i.stock_code,p.latest_price,p.price_change,p.price_change_rate from favor f,stock_info i,stock_prices p where username=#{username} and f.favor_stock_code = i.stock_code and i.stock_code = p.stock_code")
    List<FavorVo> getFavorList(String username);
}




