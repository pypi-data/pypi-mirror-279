//
// Created by haridev on 8/28/22.
//

#ifndef TAILORFS_INTERFACE_H
#define TAILORFS_INTERFACE_H
/* Internal Headers*/
#include <brahma/interface/interface_utility.h>

/* External Headers */
#include <memory>

namespace brahma {
class Interface {
 protected:
  std::shared_ptr<InterfaceUtility> utility;

 public:
  Interface();
};
}  // namespace brahma
#endif  // TAILORFS_INTERFACE_H
